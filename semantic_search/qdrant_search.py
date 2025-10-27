from vector_db.qdrant_connection import qdrant_client
from vector_db.embedding_model import embed_batch

def search_qdrant(query: str, collection_name: str, top_k: int = 3):
    query_vec = embed_batch([query])[0]
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vec,
        limit=top_k
    )
    return [r.payload.get("content", "") for r in results]
