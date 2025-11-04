# agents/router_agent.py
from .llm_intent_classifier import LLMIntentClassifier
from .structured_agent import StructuredAgent
from .unstructured_agent import UnstructuredAgent

class RouterAgent:
    def __init__(self, intent_classifier, structured_agent, unstructured_agent, schema_matcher):
        self.classifier = intent_classifier
        self.structured_agent = structured_agent
        self.unstructured_agent = unstructured_agent
        self.schema_matcher = schema_matcher

    def route(self, query: str):
        intent_info = self.classifier.classify(query)
        intent = intent_info.get("intent", "unstructured")
        print(f"[Router] Detected intent: {intent} ({intent_info.get('confidence')})")

        if intent == "structured":
            return self.structured_agent.handle(query)
        else:
            return self.unstructured_agent.handle(query)
