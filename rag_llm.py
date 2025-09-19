
import os
from groq import Groq
from retrieve import retrieve_chunks

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def rag_answer(question):
    chunks = retrieve_chunks(question)
    context = "\n\n".join(chunks)

    prompt = f"""
    You are an HR assistant. Use the provided HR documents as context.
    If the answer is not in the context, say "I don't know".

    Context:
    {context}

    Question: {question}
    Answer:
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
