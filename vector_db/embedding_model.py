import torch
from transformers import AutoTokenizer, AutoModel
from config import MODEL_NAME

# Load model once
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

def embed_batch(texts):
    """Batch-embed a list of texts."""
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings.numpy().tolist()
