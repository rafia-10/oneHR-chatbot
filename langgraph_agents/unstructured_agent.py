import requests, json
from vector_db.qdrant_connection import qdrant_client
from vector_db.embedding_model import embed_batch

class UnstructuredAgent:
    def __init__(self, openrouter_api_key: str, model="gpt-4o-mini", collection_name:str = None):
        self.api_key = openrouter_api_key
        self.model = model
        self.collection = collection_name

    def search_qdrant(self, query: str, top_k: int = 3):
        query_vec = embed_batch([query])[0]
        results = qdrant_client.search(
            collection_name=self.collection,
            query_vector=query_vec,
            limit=top_k
        )
        return [r.payload.get("content", "") for r in results]

    def summarize_results(self, query: str, contexts: list[str]):
        if not contexts:
            return "No relevant information found."

        prompt = (
            f"User question: {query}\n\n"
            f"Relevant info:\n{chr(10).join(contexts)}\n\n"
            "Summarize the relevant parts and answer clearly."
        )

        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a concise HR knowledge summarizer."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 250,
        }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)
        try:
            return res.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            return "Failed to summarize results."

    def handle(self, query: str):
        docs = self.search_qdrant(query)
        return self.summarize_results(query, docs)
