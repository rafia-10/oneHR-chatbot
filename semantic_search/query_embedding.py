from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Load the same embedding model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_text(text):
    """Embed text into a vector using Hugging Face model"""
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Mean pooling
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings[0].numpy()  # numpy array


# Example usage
user_question = "How many leave days does Kevin have?"
query_embedding = embed_text(user_question)

print("Query vector shape:", query_embedding.shape)
