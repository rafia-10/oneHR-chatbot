from ..vector_db.embedding_model import embed_batch
from ..firestore_db.firestore_schema import fetch_all_firestore_schemas
import numpy as np

class SchemaMatcher:
    """Matches user queries to Firestore DB, collection, and field using embeddings."""

    def __init__(self, db_clients: dict):
        self.db_clients = db_clients
        self.schema_cache = self._build_cache()

    def _build_cache(self):
        cache = []
        for db_name, db_client in self.db_clients.items():
            for coll, fields in fetch_all_firestore_schemas(db_client).items():
                for f in fields:
                    desc = f"{coll}.{f}"
                    cache.append({
                        "db": db_name,
                        "collection": coll,
                        "field": f,
                        "description": desc,
                        "embedding": np.array(embed_batch([desc])[0])
                    })
        return cache

    def match(self, query: str, top_k: int = 1):
        if not self.schema_cache: return []
        q_vec = np.array(embed_batch([query])[0])
        sims = [
            {**item, "similarity": np.dot(q_vec, item["embedding"]) / (np.linalg.norm(q_vec) * np.linalg.norm(item["embedding"]))}
            for item in self.schema_cache
        ]
        return sorted(sims, key=lambda x: x["similarity"], reverse=True)[:top_k]
