import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

system_it = (
    "Sei un assistente che aiuta a riscrivere email professionali "
    "in tono cordiale ma diretto. Quando ricevi un testo, restituisci "
    "tre varianti con livelli di formalità diversi."
)

system_en = (
    "You are an assistant that helps rewrite professional emails "
    "in a cordial but direct tone. When you receive a text, return "
    "three variants with different levels of formality."
)

print(f"Italiano: {len(enc.encode(system_it))} token")
print(f"English:  {len(enc.encode(system_en))} token")