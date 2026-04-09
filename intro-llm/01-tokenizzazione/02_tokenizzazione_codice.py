import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

snippet = 'print("Ciao, mondo!")'

token_ids = enc.encode(snippet)
tokens = [enc.decode([tid]) for tid in token_ids]

print(f"Stringa:  {snippet}")
print(f"N. token: {len(token_ids)}")
print(f"Pezzi:    {tokens}")