class RouterAgent:
    """Routes query to structured or unstructured agent based on LLM intent."""

    def __init__(self, threshold=0.65):
        self.threshold = threshold

    def run(self, query: str, intent_out: dict):
        intent = intent_out.get("intent")
        conf = intent_out.get("confidence", 0)
        reason = intent_out.get("reason", "")

        # default route if confidence low or invalid intent
        route = "recheck_intent"
        if conf >= self.threshold and intent in ["structured", "unstructured"]:
            route = intent

        return {
            "next_agent": route,
            "user_query": query,
            "metadata": {**intent_out, "threshold": self.threshold}
        }
