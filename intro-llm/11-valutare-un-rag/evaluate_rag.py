from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_ollama import ChatOllama, OllamaEmbeddings
from datasets import Dataset

# LLM giudice e embedder, entrambi locali via Ollama.
# Richiede: `ollama pull llama3.2` e `ollama pull nomic-embed-text`.
ollama_llm = LangchainLLMWrapper(
    ChatOllama(model="llama3.2", base_url="http://localhost:11434")
)
ollama_emb = LangchainEmbeddingsWrapper(
    OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
)

# Dataset di valutazione minimo: ogni riga ha la query,
# la risposta generata dal RAG, i chunk recuperati,
# e la risposta attesa (ground truth).
eval_data = {
    "question": [
        "Qual è il timeout di default delle richieste API?",
        "Come si configura l'autenticazione?",
        "Quali endpoint supportano il metodo PUT?",
    ],
    "answer": [
        "Il timeout di default è 30 secondi, configurabile con request_timeout.",
        "L'autenticazione richiede un token Bearer nell'header Authorization.",
        "Gli endpoint /users e /products supportano PUT per aggiornamenti.",
    ],
    "contexts": [
        [
            "Il timeout delle richieste è configurabile con il parametro "
            "request_timeout, espresso in secondi. Il default è 30 secondi."
        ],
        [
            "L'autenticazione API richiede un token Bearer nel header "
            "Authorization. Il token scade dopo 24 ore."
        ],
        [
            "Gli endpoint API sono raggruppati in categorie: /users per "
            "gestione utenti, /products per prodotti, /orders per ordini."
        ],
    ],
    "ground_truth": [
        "Il timeout di default è 30 secondi.",
        "Si usa un token Bearer nell'header Authorization.",
        "La documentazione non specifica quali endpoint supportano PUT.",
    ],
}

dataset = Dataset.from_dict(eval_data)

results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_recall, context_precision],
    llm=ollama_llm,
    embeddings=ollama_emb,
)

print(results)
