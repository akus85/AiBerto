import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

model_id = "Qwen/Qwen2.5-7B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
)

prompt = "Spiega in due frasi cosa è la quantizzazione di un modello."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
output_ids = model.generate(**inputs, max_new_tokens=120)

print(tokenizer.decode(output_ids[0], skip_special_tokens=True))