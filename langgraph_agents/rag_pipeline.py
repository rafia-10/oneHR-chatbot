# agents/router_agent.py
from .llm_intent_classifier import LLMIntentClassifier
from .structured_agent import StructuredAgent
from .unstructured_agent import UnstructuredAgent

class RouterAgent:
    def __init__(self, openrouter_api_key: str):
        self.classifier = LLMIntentClassifier(openrouter_api_key)
        self.structured_agent = StructuredAgent(openrouter_api_key)
        self.unstructured_agent = UnstructuredAgent(openrouter_api_key)

    def route(self, query: str):
        intent_info = self.classifier.classify(query)
        intent = intent_info.get("intent", "unstructured")
        print(f"[Router] Detected intent: {intent} ({intent_info.get('confidence')})")

        if intent == "structured":
            return self.structured_agent.handle(query)
        else:
            return self.unstructured_agent.handle(query)
