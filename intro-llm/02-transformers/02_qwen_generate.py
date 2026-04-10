from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

prompt = "Spiega in due frasi cosa è un token in un LLM."

inputs = tokenizer(prompt, return_tensors="pt")
output_ids = model.generate(
    **inputs,
    max_new_tokens=80,
    temperature=0.7,
    do_sample=True,
)
response = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print(response)