import requests
from firestore_db.firebase_connect import db_clients

class StructuredAgent:
    """Fetch numeric data from Firestore and summarize via LLM."""

    def __init__(self, openrouter_api_key: str, model="gpt-4o-mini"):
        self.api_key = openrouter_api_key
        self.model = model

    def summarize(self, query: str, result: dict) -> str:
        if not result.get("value"):
            return "No numeric data found."
        prompt = (
            f"User question: {query}\n"
            f"Numeric results: {result['value']}\n"
            "Summarize concisely."
        )
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": "You are a concise HR summarizer."},
                         {"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 200,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers, timeout=15)
            return res.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            return "Failed to summarize numeric results."

    def run(self, query: str, schema: dict) -> dict:
        if not schema:
            return {"value": None, "aggregation": None, "error": "No schema provided"}

        db = db_clients.get(schema["db"])
        if not db:
            return {"value": None, "aggregation": None, "error": f"DB {schema['db']} not found"}

        try:
            values = [d.to_dict()[schema["field"]] for d in db.collection(schema["collection"]).stream()
                      if schema["field"] in d.to_dict() and isinstance(d.to_dict()[schema["field"]], (int, float))]

            if not values:
                return {"value": None, "aggregation": None, "error": "No numeric data"}

            result = {"value": {"count": len(values), "sum": sum(values), "average": sum(values)/len(values)},
                      "aggregation": "count/sum/average",
                      "summary": self.summarize(query, {"value": {"count": len(values), "sum": sum(values), "average": sum(values)/len(values)}})}
            return result
        except Exception as e:
            return {"value": None, "aggregation": None, "error": str(e)}
