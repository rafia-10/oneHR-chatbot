import torch
from transformers import AutoTokenizer, AutoModel
from config import MODEL_NAME

# Load model once
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

def embed_batch(texts: list):
    """
    Embed a list of texts into vectors using Hugging Face model.
    Can also embed a single text by passing [text].
    Returns a list of numpy arrays.
    """
    if not texts:
        return []

    encoded = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        out = model(**encoded)

    # mean pooling
    embeddings = out.last_hidden_state.mean(dim=1).numpy()
    return embeddings.tolist()
