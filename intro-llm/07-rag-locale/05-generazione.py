import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float32,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
llm = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
)


def genera_risposta(messaggi: list[dict], max_tokens: int = 512) -> str:
    input_text = tokenizer.apply_chat_template(
        messaggi, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(input_text, return_tensors="pt").to(llm.device)

    output_ids = llm.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=False,
    )
    nuovi_token = output_ids[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(nuovi_token, skip_special_tokens=True)


if __name__ == "__main__":
    messaggi = [
        {"role": "system", "content": "Sei un assistente tecnico conciso."},
        {"role": "user", "content": "Spiega in due righe cos'e' la quantizzazione."},
    ]
    print(genera_risposta(messaggi, max_tokens=200))
