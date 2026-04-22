from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np

# Modello bi-encoder: encoda query e documenti separatamente
bi_encoder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Cross-encoder: valuta la rilevanza dell'accoppiamento query-documento
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Cinque chunk simulati su API configuration (scenario del cappello)
chunks = [
    {
        "id": 1,
        "text": "L'autenticazione API richiede un token Bearer nel header Authorization. "
                "Il token deve essere preceduto dalla stringa 'Bearer ' e deve essere separato dal valore "
                "con uno spazio. Il token scade dopo 24 ore e deve essere rigenerato."
    },
    {
        "id": 2,
        "text": "Il rate limiting è implementato per proteggere il servizio da abusi. "
                "Ogni client riceve un limite di 1000 richieste per ora. "
                "Se il limite è superato, il server risponde con uno stato 429 Too Many Requests. "
                "I dettagli sul limite rimasto sono negli header X-RateLimit-Remaining."
    },
    {
        "id": 3,
        "text": "Gli endpoint API sono raggruppati in categorie: /users per gestione utenti, /products per prodotti, "
                "/orders per ordini, /settings per la configurazione del server. "
                "Ogni endpoint accetta solo i metodi HTTP documentati nel reference. "
                "Richieste con metodi non supportati restituiscono 405 Method Not Allowed."
    },
    {
        "id": 4,
        "text": "La dimensione massima del pool di connessioni è configurabile nel parametro max_connections. "
                "Il default è 10. Valori più alti aumentano la concorrenza ma consumano più memoria. "
                "Per workload alto è raccomandato un valore tra 50 e 100."
    },
    {
        "id": 5,
        "text": "Il timeout delle richieste è configurabile con il parametro request_timeout, espresso in secondi. "
                "Il default è 30 secondi. Se una richiesta non riceve risposta entro questo tempo, "
                "viene interrotta e il client riceve un'eccezione TimeoutError. "
                "Per operazioni lunghe, aumentare questo valore è consigliato."
    },
]

query = "come si configura il timeout delle richieste API"

# FASE 1: Bi-encoder ranking (ricerca vettoriale)
print("=" * 70)
print("RANKING CON BI-ENCODER (cosine similarity)")
print("=" * 70)

query_embedding = bi_encoder.encode(query, normalize_embeddings=True)
chunk_texts = [chunk["text"] for chunk in chunks]
chunk_embeddings = bi_encoder.encode(chunk_texts, normalize_embeddings=True)

# Calcola similarity cosine tra query e ogni chunk
scores_bi = (chunk_embeddings @ query_embedding).tolist()

# Crea lista di (chunk_id, testo, score) ordinata per score
bi_results = sorted(
    [(chunks[i]["id"], chunk_texts[i][:80] + "...", scores_bi[i]) for i in range(len(chunks))],
    key=lambda x: x[2],
    reverse=True
)

for rank, (chunk_id, text_preview, score) in enumerate(bi_results, 1):
    print(f"{rank}. Chunk {chunk_id} (score: {score:.4f})")
    print(f"   {text_preview}\n")

# FASE 2: Cross-encoder reranking
print("=" * 70)
print("RANKING CON CROSS-ENCODER (rilevanza query-documento)")
print("=" * 70)

# Passa a cross-encoder le coppie (query, documento)
query_chunk_pairs = [[query, text] for text in chunk_texts]
scores_cross = cross_encoder.predict(query_chunk_pairs)

# Crea lista di (chunk_id, testo, score) ordinata per score di cross-encoder
cross_results = sorted(
    [(chunks[i]["id"], chunk_texts[i][:80] + "...", scores_cross[i]) for i in range(len(chunks))],
    key=lambda x: x[2],
    reverse=True
)

for rank, (chunk_id, text_preview, score) in enumerate(cross_results, 1):
    print(f"{rank}. Chunk {chunk_id} (score: {score:.4f})")
    print(f"   {text_preview}\n")

# Mostra come il ranking cambia
print("=" * 70)
print("CONFRONTO: CAMBIAMENTO DI POSIZIONE")
print("=" * 70)

bi_positions = {item[0]: rank for rank, item in enumerate(bi_results, 1)}
cross_positions = {item[0]: rank for rank, item in enumerate(cross_results, 1)}

for chunk_id in range(1, 6):
    before = bi_positions[chunk_id]
    after = cross_positions[chunk_id]
    direction = "↑" if after < before else "↓" if after > before else "="
    print(f"Chunk {chunk_id}: posizione {before} → {after}  {direction}")

print("\n[Atteso: il Chunk 5 (timeout) sale da basso nel ranking vettoriale al primo dopo reranking]")