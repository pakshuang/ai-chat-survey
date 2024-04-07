import argparse
import logging
import pathlib

import pandas as pd
import torch
from datasets import Dataset, DatasetDict
from peft import (
    AutoPeftModelForCausalLM,
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    GenerationConfig,
    GPTQConfig,
    Trainer,
    TrainingArguments,
)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Training model")

    parser.add_argument(
        "--base",
        dest="base_model",
        type=str,
        help="Base model (huggingface name or path to GPTQ folder) to finetune",
    )
    parser.add_argument(
        "--dataset-path",
        dest="dataset",
        type=str,
        help="path to dataset. Dataset MUST contain columns `input` and `output` and if needed, `system`",
    )
    parser.add_argument(
        "--bits", dest="bits", type=int, help="Number of bits of quantised model"
    )

    parser.add_argument(
        "--output-path",
        dest="output",
        type=str,
        help="Output path",
        default=str(pathlib.Path(__file__).parent.resolve()) + "/../../backend/models",
    )
    parser.add_argument(
        "--learning-rate", dest="lr", type=float, help="Learning rate", default=2.5e-4
    )
    parser.add_argument(
        "--steps", dest="steps", type=int, help="Number of steps to train", default=256
    )
    parser.add_argument("--r", dest="r", type=int, help="rank parameter", default=16)
    parser.add_argument(
        "--lora-dropout",
        dest="dropout",
        type=float,
        help="dropout parameter",
        default=0.05,
    )
    parser.add_argument(
        "--lora-alpha", dest="alpha", type=int, help="dropout parameter", default=16
    )
    parser.add_argument(
        "--train-size",
        dest="train",
        type=float,
        help="size of training dataset as a proportion (0-1)",
        default=0.75,
    )
    parser.add_argument(
        "--has-system-prompt",
        dest="has_sys",
        type=int,
        help="Does the model support system prompts in their chat template 1 or 0",
        default=1,
    )
    parser.add_argument(
        "--max-len", dest="max_len", type=int, help="Max generation length", default=256
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="Seed used when splitting dataset. The value -1 will be interpreted as an un-set seed",
        default=-1,
    )
    parser.add_argument(
        "--group_size", type=int, default=128, help="Specify GPTQ group_size."
    )
    # Parse the arguments
    args = parser.parse_args()

    # Access the argument values

    gptq_config = GPTQConfig(bits=args.bits, disable_exllama=True)

    base = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        quantization_config=gptq_config,
        device_map="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(
        args.base_model,
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id

    base.gradient_checkpointing_enable()
    base = prepare_model_for_kbit_training(base)

    config = LoraConfig(
        r=args.r,
        lora_alpha=args.alpha,
        target_modules=[
            "q_proj",
            "k_proj",
            "down_proj",
            "v_proj",
            "gate_proj",
            "o_proj",
            "up_proj",
        ],
        lora_dropout=args.dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(base, config)
    model.config.use_cache = False
    df = pd.read_csv(args.dataset)
    ds = Dataset.from_pandas(df)
    if args.seed == -1:
        ds_splits = split_dataset(ds, args)
    else:
        ds_splits = split_dataset(ds, args, seed=args.seed)

    train = ds_splits["train"].map(
        lambda row: {
            "input_ids": format_input_outputs(
                row, args.has_sys, tokenizer, args.max_len
            )
        }
    )
    test = ds_splits["test"].map(
        lambda row: {
            "input_ids": format_input_outputs(
                row, args.has_sys, tokenizer, args.max_len
            )
        }
    )
    valid = ds_splits["valid"].map(
        lambda row: {
            "input_ids": format_input_outputs(
                row, args.has_sys, tokenizer, args.max_len
            )
        }
    )

    trainer = Trainer(
        model=model,
        train_dataset=train,
        eval_dataset=valid,
        args=TrainingArguments(
            output_dir=args.output,
            warmup_steps=1,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=1,
            gradient_checkpointing=True,
            max_steps=args.steps,
            learning_rate=args.lr,  # Want a small lr for finetuning
            evaluation_strategy="no",
            eval_steps=25,
            optim="paged_adamw_8bit",
            logging_steps=25,
            save_strategy="no",
            load_best_model_at_end=True,
        ),
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )
    trainer.train()
    trainer.model.save_pretrained(args.output)

    logging.warning(
        """Your model has been finetuned and the LORA adapters can now be found in backend/models/. 
                    Continuing this script will require more VRAM. The following portion may not function properly without >=8GB of VRAM."""
    )
    # Test inference.

    persisted_model = AutoPeftModelForCausalLM.from_pretrained(
        str(pathlib.Path(__file__).parent.resolve()) + "/../../backend/models",
        low_cpu_mem_usage=True,
        return_dict=True,
        torch_dtype=torch.float16,
        device_map="cuda",
    )

    generation_config = GenerationConfig(
        penalty_alpha=0.6,
        do_sample=True,
        top_k=5,
        temperature=0.5,
        repetition_penalty=1.2,
        max_new_tokens=args.max_len,
    )
    for row in ds_splits["test"]:
        print(args.has_sys)

        if args.has_sys:
            messages = [
                {"role": "system", "content": row["system"]},
                {"role": "user", "content": row["input"]},
            ]

        else:
            messages = [{"role": "user", "content": row["input"]}]

        for_gen = tokenizer.apply_chat_template(
            messages, return_tensors="pt", tokenize=False
        )

        encoding = tokenizer(
            for_gen,
            truncation=True,
            max_length=args.max_len,
            padding="max_length",
            return_tensors="pt",
        ).to("cuda")

        outputs = persisted_model.generate(
            input_ids=encoding.input_ids,
            attention_mask=encoding.attention_mask,
            generation_config=generation_config,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )
        print(tokenizer.decode(outputs[0], skip_special_tokens=True))


def split_dataset(ds: Dataset, args: argparse.ArgumentParser, seed: int = 1):
    ds_train_devtest = ds.train_test_split(test_size=1 - args.train, seed=seed)
    ds_devtest = ds_train_devtest["test"].train_test_split(test_size=0.5, seed=seed)
    ds_splits = DatasetDict(
        {
            "train": ds_train_devtest["train"],
            "valid": ds_devtest["train"],
            "test": ds_devtest["test"],
        }
    )
    return ds_splits


def format_input_outputs(row, has_sys: bool, tokenizer, max_len: int):

    if has_sys:
        messages = [
            {"role": "system", "content": row["system"]},
            {"role": "user", "content": row["input"]},
            {"role": "assistant", "content": row["output"]},
        ]

    else:
        messages = [
            {"role": "user", "content": row["input"]},
            {"role": "assistant", "content": row["output"]},
        ]

    formatted = tokenizer.apply_chat_template(messages, tokenize=False)
    result = tokenizer(
        formatted,
        truncation=True,
        max_length=max_len,
        padding="max_length",
    )

    return result["input_ids"].copy()


if __name__ == "__main__":
    main()
