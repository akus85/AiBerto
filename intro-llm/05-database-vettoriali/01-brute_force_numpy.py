import numpy as np
from sentence_transformers import SentenceTransformer

corpus = [
    "La distanza del coseno misura l'angolo tra due vettori, ignorando la magnitudine.",
    "HNSW è un algoritmo di nearest neighbor approssimato basato su un grafo multi-livello.",
    "Il product quantization comprime i vettori dividendoli in sottovettori quantizzati.",
    "BM25 è un algoritmo di ranking basato sulla frequenza dei termini in stile TF-IDF.",
    "Reciprocal Rank Fusion combina classifiche diverse sommando il reciproco delle posizioni.",
]

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Normalizzo a norma 1: il prodotto scalare tra vettori normalizzati
# è identico alla similarità del coseno, e numpy lo esegue molto velocemente.
corpus_embeddings = model.encode(corpus, normalize_embeddings=True)
corpus_matrix = np.asarray(corpus_embeddings, dtype=np.float32)

def search(query: str, k: int = 3):
    query_embedding = model.encode(query, normalize_embeddings=True)
    scores = corpus_matrix @ query_embedding
    top_k = np.argsort(-scores)[:k]
    return [(corpus[i], float(scores[i])) for i in top_k]

for text, score in search("come funziona HNSW?"):
    print(f"{score:.3f}  {text}")