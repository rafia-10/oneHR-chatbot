import requests
from semantic_search.qdrant_search import search_qdrant
class UnstructuredAgent:
    def __init__(self, openrouter_api_key: str, model="gpt-4o-mini", collection_name: str = None):
        self.api_key = openrouter_api_key
        self.model = model
        self.collection = collection_name

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
        docs = search_qdrant(query, self.collection)
        return self.summarize_results(query, docs)
