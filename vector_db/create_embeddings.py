# vector_db/create_embeddings.py
from transformers import AutoTokenizer, AutoModel
import torch
import json
from fields2push_dev import fields_to_embed_dev
from fields2push_internal import fields_to_embed_internal

# --- Load the embedding model ---
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_text(text):
    """Return embedding vector for a given text."""
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.last_hidden_state.mean(dim=1)  # mean pooling
    return embeddings[0].numpy()

def create_embeddings(fields_list):
    """Embed all fields in a list."""
    embeddings_list = []
    for field in fields_list:
        emb = embed_text(field["value"])
        embeddings_list.append({
            "field_name": field["field_name"],
            "embedding": emb.tolist()
        })
    return embeddings_list

# --- Dev fields ---
dev_embeddings = create_embeddings(fields_to_embed_dev)
with open("vector_db/dev_fields_embeddings.json", "w") as f:
    json.dump(dev_embeddings, f)
print(f"✅ Dev: {len(dev_embeddings)} fields embedded")

# --- Internal fields ---
internal_embeddings = create_embeddings(fields_to_embed_internal)
with open("vector_db/internal_fields_embeddings.json", "w") as f:
    json.dump(internal_embeddings, f)
print(f"✅ Internal: {len(internal_embeddings)} fields embedded")
