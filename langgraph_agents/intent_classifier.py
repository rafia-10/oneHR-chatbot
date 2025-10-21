from langgraph.nodes import Node
import numpy as np
from vector_db.embedding_model import embed_batch
from firestore_db.firestore_schema import fetch_all_firestore_schemas

class DynamicIntentClassifier(Node):
    def __init__(self, db_clients, similarity_threshold=0.6):
        """
        db_clients: dict of Firestore clients, e.g.,
          {"dev": db_dev, "internal": db_internal}

        similarity_threshold: cosine similarity threshold for structured detection
        """
        self.db_clients = db_clients
        self.similarity_threshold = similarity_threshold

        # Fetch schemas dynamically from all DBs
        self.schemas = fetch_all_firestore_schemas(db_clients)

        # Precompute embeddings for all fields
        self.field_texts = [
            f"{s['db']}.{s['collection']}.{s['field']}: {s.get('description', '')}"
            for s in self.schemas
        ]
        self.field_embeddings = np.array(embed_batch(self.field_texts))

    def run(self, user_query: str):
        """
        Returns:
        intent: "structured" or "unstructured"
        matched_schema: dict with keys: db, collection, field, description
        confidence: cosine similarity score
        """
        query_emb = np.array(embed_batch([user_query]))[0]

        sims = np.dot(self.field_embeddings, query_emb) / (
            np.linalg.norm(self.field_embeddings, axis=1) * np.linalg.norm(query_emb)
        )
        best_idx = int(np.argmax(sims))
        best_score = sims[best_idx]

        if best_score >= self.similarity_threshold:
            intent = "structured"
            matched_schema = self.schemas[best_idx]
        else:
            intent = "unstructured"
            matched_schema = None

        return intent, matched_schema, float(best_score)
