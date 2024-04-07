import argparse
from datasets import Dataset, DatasetDict
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, get_peft_model, prepare_model_for_kbit_training, PeftModel


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Training model')


    parser.add_argument('--base', dest='base_model', type=str, help='Base model (huggingface name or path) to finetune')
    parser.add_argument('--dataset-path', dest='dataset', type=str, help='path to dataset. Dataset MUST contain columns `input` and `output` and if needed, `system`')
    parser.add_argument('--output-path', dest='output', type=str, help='Output path')

    parser.add_argument('--learning-rate', dest='lr', type=float, help='Learning rate', default=2.5e-4)
    parser.add_argument('--steps', dest='steps', type=int, help='Number of steps to train', default=256)
    parser.add_argument('--r', dest='r', type=int, help='rank parameter', default=16)
    parser.add_argument('--lora-dropout', dest='dropout', type=float, help='dropout parameter', default=0.05)
    parser.add_argument('--lora-alpha', dest='alpha', type=int, help='dropout parameter', default=16)
    parser.add_argument('--train-size', dest='train', type=float, help='size of training dataset as a proportion (0-1)', default=0.75)
    parser.add_argument('--system', dest='has_sys', type=int, help='Does the model support system prompts in their chat template 1 or 0', default=1)
    parser.add_argument('--max-len', dest='max_len', type=int, help='Max generation length', default=256)

    # Parse the arguments
    args = parser.parse_args()

    # Access the argument values
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype="float16",
    )
    print("Loading model...")
    base = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        quantization_config=bnb_config,
        trust_remote_code=True,
        device_map="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(
        args.base_model, 
        trust_remote_code=True, 
        return_token_type_ids=False
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    base.gradient_checkpointing_enable()
    base = prepare_model_for_kbit_training(base)

    config = LoraConfig(
        r=args.r,
        lora_alpha=args.alpha,
        target_modules=['q_proj', 'k_proj', 'down_proj', 'v_proj', 'gate_proj', 'o_proj', 'up_proj'], 
        lora_dropout=args.dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(base, config)

    # Dataset stuf
    df = pd.read_csv(args.dataset)
    ds = Dataset.from_pandas(df)
   
    ds_splits = split_dataset(ds, args)
    
    train = ds_splits["train"].map(lambda row: {'input_ids': format_input_outputs(row, args.has_sys, tokenizer, args.max_len)})
    test = ds_splits["test"].map(lambda row: {'input_ids': format_input_outputs(row, args.has_sys, tokenizer, args.max_len)})
    valid = ds_splits["valid"].map(lambda row: {'input_ids': format_input_outputs(row, args.has_sys, tokenizer, args.max_len)})

    print("Training")

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
        learning_rate=args.lr, # Want a small lr for finetuning
        evaluation_strategy = 'no',
        eval_steps=25,
        optim="paged_adamw_8bit",
        logging_steps=25,                  
        save_strategy="no",       
        load_best_model_at_end=True,            
        ),
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    
    )
    trainer.train()

 
    # Your script logic here

def split_dataset(ds: Dataset, args: argparse.ArgumentParser):
    ds_train_devtest = ds['train'].train_test_split(test_size=1-args.train, seed=42)
    ds_devtest = ds_train_devtest['test'].train_test_split(test_size=0.5, seed=42)
    ds_splits = DatasetDict({
        'train': ds_train_devtest['train'],
        'valid': ds_devtest['train'],
        'test': ds_devtest['test']
    })
    return ds_splits

def format_input_outputs(row, has_sys: bool, tokenizer, max_len: int):
    if has_sys:
        messages = [
            {
                "role": "system", "content": row["system"]
            },
            {
                "role": "user", "content": row["input"]
            },
            {
                "role": "assistant", "content": row["output"]
            }
        ]

    else:
        messages = [
            {
                "role": "user", "content": row["input"]
            },
            {
                "role": "assistant", "content": row["output"]
            }
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