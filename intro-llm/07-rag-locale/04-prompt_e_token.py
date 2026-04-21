from transformers import AutoTokenizer

import importlib

retrieval = importlib.import_module("03-retrieval")
recupera = retrieval.recupera

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
CONTEXT_WINDOW = 32768
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def costruisci_prompt(domanda: str, contesti: list[tuple]) -> list[dict]:
    blocchi = []
    for testo, meta, dist in contesti:
        intestazione = " > ".join(
            v for k, v in sorted(meta.items())
            if k in ("titolo", "sezione", "sottosezione")
        )
        blocchi.append(f"[Fonte: {intestazione}]\n{testo}")

    contesto_formattato = "\n\n---\n\n".join(blocchi)

    return [
        {
            "role": "system",
            "content": (
                "Sei un assistente tecnico. Rispondi alla domanda dell'utente "
                "usando esclusivamente le informazioni contenute nel contesto "
                "fornito. Se il contesto non contiene la risposta, dillo "
                "esplicitamente. Non inventare informazioni."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Contesto:\n\n{contesto_formattato}\n\n"
                f"Domanda: {domanda}"
            ),
        },
    ]


def conta_token_prompt(messaggi: list[dict]) -> int:
    testo_completo = tokenizer.apply_chat_template(messaggi, tokenize=False)
    return len(tokenizer.encode(testo_completo))


if __name__ == "__main__":
    domanda = "come si gestiscono le eccezioni?"
    contesti = recupera(domanda, k=3)
    messaggi = costruisci_prompt(domanda, contesti)

    token_usati = conta_token_prompt(messaggi)
    print(f"Token nel prompt: {token_usati}")
    print(f"Token rimanenti per la risposta: {CONTEXT_WINDOW - token_usati}")
