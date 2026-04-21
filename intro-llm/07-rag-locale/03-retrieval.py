import sys

import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "./rag_db"
COLLECTION_NAME = "documenti"
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

model = SentenceTransformer(EMBED_MODEL)
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(name=COLLECTION_NAME)


def recupera(domanda: str, k: int = 3):
    query_embedding = model.encode(
        [domanda], normalize_embeddings=True
    ).tolist()
    risultati = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
    )
    return list(zip(
        risultati["documents"][0],
        risultati["metadatas"][0],
        risultati["distances"][0],
    ))


if __name__ == "__main__":
    domanda = " ".join(sys.argv[1:]) or "come si gestiscono le eccezioni?"
    for testo, meta, dist in recupera(domanda):
        print(f"[{dist:.3f}] ({meta.get('sezione', '?')}) {testo[:100]}...")
