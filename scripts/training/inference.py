from peft import AutoPeftModelForCausalLM
import torch
import pathlib

persisted_model = AutoPeftModelForCausalLM.from_pretrained(
    str(pathlib.Path(__file__).parent.resolve()) + "/../../backend/models",
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map="cuda",
)
