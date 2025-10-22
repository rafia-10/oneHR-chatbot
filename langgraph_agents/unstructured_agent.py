from vector_db.qdrant_connection import client as qdrant_client
from vector_db.embedding_model import embed_batch

class UnstructuredAgent:
    """
    Searches Qdrant for top-k relevant unstructured documents.
    """

    def run(self, query: str, top_k: int = 3, collection_name: str = None):
        # 1️⃣ Embed the user query
        q_vec = embed_batch([query])[0]

        # 2️⃣ Search Qdrant
        search_res = qdrant_client.search(
            collection_name=collection_name,
            query_vector=q_vec,
            limit=top_k
        )

        # 3️⃣ Format results
        results = [{"id": r.id, "payload": r.payload, "score": r.score} for r in search_res]
        return results
