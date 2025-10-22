# Predefined examples (few-shot learning)
examples = [
    {
        "q": "What's the average headcount in engineering?",
        "intent": "structured",
        "reason": "Asks for numeric metric stored in database."
    },
    {
        "q": "Show me the sum of salaries for sales department.",
        "intent": "structured",
        "reason": "Requires aggregation from numeric field."
    },
    {
        "q": "What are the common themes in exit interviews?",
        "intent": "unstructured",
        "reason": "Asks for qualitative insights from text data."
    },
    {
        "q": "Summarize feedback from the latest employee surveys.",
        "intent": "unstructured",
        "reason": "Requests sentiment or thematic summary."
    },
    {
        "q": "How many people joined last quarter?",
        "intent": "structured",
        "reason": "Requests a count — numeric metric."
    },
]

def build_prompt(query: str):
    """
    Construct a well-structured prompt with examples and JSON output instruction.
    """
    examples_text = "\n".join([
        f"Q: {ex['q']}\nA: intent={ex['intent']}, reason={ex['reason']}"
        for ex in examples
    ])

    prompt = f"""
    You are an **HR analytics intent classifier**.
    Your job: decide whether a user query is asking for structured (numeric/database) 
    or unstructured (textual/semantic) data.

    Rules:
    - "Structured" = numeric, countable, measurable, or stored in database fields (e.g., headcount, salary, average age).
    - "Unstructured" = descriptive, qualitative, or feedback-related (e.g., interview responses, text comments, reasons).

    Be concise, deterministic, and only output JSON.

    {examples_text}

    Q: {query}
    A: Provide JSON like:
    {{
    "intent": "structured" | "unstructured",
    "reason": "brief reasoning",
    "confidence": 0.0–1.0
    }}
    """
    return prompt.strip()