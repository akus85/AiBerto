import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="manuali_tecnici",
    metadata={"hnsw:space": "cosine"},
)

# Calcolo gli embedding esplicitamente con sentence-transformers.
# Lo stesso modello in insert e in query è una delle regole più importanti.
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

documenti = [
    {
        "id": "chunk-001",
        "text": "HNSW costruisce un grafo multi-livello per la ricerca approssimata.",
        "metadata": {"fonte": "manuale_ann", "sezione": "indici", "lingua": "it"},
    },
    {
        "id": "chunk-002",
        "text": "Il product quantization comprime i vettori in sottovettori quantizzati.",
        "metadata": {"fonte": "manuale_ann", "sezione": "compressione", "lingua": "it"},
    },
    {
        "id": "chunk-003",
        "text": "BM25 è un algoritmo di ranking basato sulla frequenza dei termini.",
        "metadata": {"fonte": "manuale_ir", "sezione": "ranking", "lingua": "it"},
    },
    {
        "id": "chunk-004",
        "text": "La similarità del coseno misura l'angolo tra due vettori.",
        "metadata": {"fonte": "manuale_ann", "sezione": "metriche", "lingua": "it"},
    },
]

embeddings = model.encode(
    [d["text"] for d in documenti],
    normalize_embeddings=True,
).tolist()

collection.add(
    ids=[d["id"] for d in documenti],
    documents=[d["text"] for d in documenti],
    embeddings=embeddings,
    metadatas=[d["metadata"] for d in documenti],
)

# Query: cerco i tre passaggi più simili, ma solo dal manuale ANN.
query = "come funzionano gli indici approssimati?"
query_embedding = model.encode([query], normalize_embeddings=True).tolist()

risultati = collection.query(
    query_embeddings=query_embedding,
    n_results=3,
    where={"fonte": "manuale_ann"},
)

for doc, meta, dist in zip(
    risultati["documents"][0],
    risultati["metadatas"][0],
    risultati["distances"][0],
):
    print(f"[{dist:.3f}] ({meta['sezione']}) {doc}")