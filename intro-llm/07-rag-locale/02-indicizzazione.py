import pickle
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path("chunks.pkl")
DB_PATH = "./rag_db"
COLLECTION_NAME = "documenti"
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

with CHUNKS_PATH.open("rb") as f:
    chunks = pickle.load(f)

model = SentenceTransformer(EMBED_MODEL)

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)

ids = [f"chunk-{i}" for i in range(len(chunks))]
testi = [c.page_content for c in chunks]
metadatas = [c.metadata if c.metadata else {"sezione": "sconosciuta"} for c in chunks]
embeddings = model.encode(testi, normalize_embeddings=True).tolist()

collection.add(
    ids=ids,
    documents=testi,
    embeddings=embeddings,
    metadatas=metadatas,
)

print(f"Indicizzati {len(ids)} chunk in ChromaDB ({DB_PATH})")
