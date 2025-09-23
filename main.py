# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from rag_llm import rag_answer

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(req: ChatRequest):
    answer = rag_answer(req.question)
    return {"answer": answer}
