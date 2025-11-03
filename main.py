import os
from langgraph_agents.llm_intent_classifier import LLMIntentClassifier
from langgraph_agents.rag_pipeline import  RouterAgent
from langgraph_agents.structured_agent import StructuredAgent
from langgraph_agents.unstructured_agent import UnstructuredAgent
from semantic_search.schema_matcher import SchemaMatcher

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

# 1️⃣ Initialize agents
intent_clf = LLMIntentClassifier(openrouter_api_key=OPENROUTER_KEY)
structured_agent = StructuredAgent(openrouter_api_key=OPENROUTER_KEY)
unstructured_agent = UnstructuredAgent(openrouter_api_key=OPENROUTER_KEY, collection_name="dev_fields")

# 2️⃣ Schema matcher for structured queries
schema_matcher = SchemaMatcher()

# 3️⃣ RAG pipeline
pipeline = RouterAgent(
    intent_classifier=intent_clf,
    structured_agent=structured_agent,
    unstructured_agent=unstructured_agent,
    schema_matcher=schema_matcher
)

# 4️⃣ Test queries
queries = [
    "How many employees joined last month?",
    "What are common reasons for leaving in exit interviews?",
]

for q in queries:
    output = pipeline.run(q)
    print(f"Query: {q}")
    print(f"Output:\n{output}\n{'-'*50}\n")
