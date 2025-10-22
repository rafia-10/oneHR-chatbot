import requests, json, time
from intent_classifier_utils import build_prompt

class LLMIntentClassifier:
    """
    Classifies a user query as 'structured' or 'unstructured'
    using an OpenRouter LLM (e.g., GPT-4o-mini, Claude, Mistral, etc.)

    Example return:
    {
        "intent": "structured",
        "confidence": 0.93,
        "reason": "User asked for numeric data (average salary)"
    }
    """

    def __init__(self, openrouter_api_key: str, model: str = "gpt-4o-mini", max_retries: int = 2):
        self.api_key = openrouter_api_key
        self.model = model
        self.max_retries = max_retries
    

    def classify(self, query: str):
        """
        Calls OpenRouter API to classify the query.
        Retries gracefully and falls back to heuristic if needed.
        """
        if not query or not isinstance(query, str):
            return {"intent": "unstructured", "confidence": 0.0, "reason": "invalid query"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a precise and reliable intent classifier for HR analytics."},
                {"role": "user", "content": build_prompt(query)},
            ],
            "temperature": 0,
            "max_tokens": 200,
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers, timeout=20)
                response.raise_for_status()
                data = response.json()
                text = data["choices"][0]["message"]["content"]

                # Try to parse JSON cleanly
                try:
                    result = json.loads(text)
                    if "intent" in result:
                        result.setdefault("confidence", 0.9)
                        return result
                except json.JSONDecodeError:
                    pass

                # fallback keyword detection
                if "structured" in text.lower():
                    return {"intent": "structured", "confidence": 0.7, "reason": "keyword fallback"}
                if "unstructured" in text.lower():
                    return {"intent": "unstructured", "confidence": 0.7, "reason": "keyword fallback"}

            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1.5)
                    continue
                return {"intent": "unstructured", "confidence": 0.0, "reason": f"error: {str(e)}"}

        # If all fails
        return {"intent": "unstructured", "confidence": 0.0, "reason": "classification failed"}

