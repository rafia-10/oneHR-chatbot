from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import json


model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
with open("rag_chunks.json", "r") as f:
    rag_chunks = json.load(f)


def embed_text(text):
    # Tokenize and get embeddings
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    
    # Mean pooling
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings[0].numpy()  # convert to numpy array


# embed all the chunks

rag_embeddings = []

for chunk in rag_chunks:
    emb = embed_text(chunk["text"])
    rag_embeddings.append({
        "id": chunk["id"],
        "companyId": chunk["companyId"],
        "collection": chunk["collection"],
        "embedding": emb.tolist()  # JSON-safe
    })

# Save to file
with open("rag_embeddings.json", "w") as f:
    json.dump(rag_embeddings, f)
