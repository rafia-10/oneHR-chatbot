# vector_db/create_embeddings.py
import json
import torch
from transformers import AutoTokenizer, AutoModel
from firebase_connect import db_dev, db_internal
from fields2push_dev import fields_to_embed_dev
from fields2push_internal import fields_to_embed_internal

# --- Load embedding model once ---
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_batch(texts):
    """Batch-embed a list of texts."""
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings.numpy().tolist()

def fetch_and_embed(db, fields_to_embed, company_name):
    """Fetch Firestore text fields, embed them, and save results."""
    all_embeddings = []
    batch_texts, batch_meta = [], []

    for collection_name, fields in fields_to_embed.items():
        print(f"📦 Fetching from collection: {collection_name}")
        docs = db.collection(collection_name).stream()

        for doc in docs:
            data = doc.to_dict() or {}
            for field in fields:
                if field not in data or not data[field]:
                    continue

                # Convert any non-string (list/dict/num) to string
                value = data[field]
                if not isinstance(value, str):
                    value = json.dumps(value, ensure_ascii=False)

                batch_texts.append(value)
                batch_meta.append({
                    "collection": collection_name,
                    "field_name": field,
                    "text": value
                })

                # Process in batches for efficiency
                if len(batch_texts) >= 32:
                    vectors = embed_batch(batch_texts)
                    for meta, vector in zip(batch_meta, vectors):
                        meta["embedding"] = vector
                        all_embeddings.append(meta)
                    batch_texts, batch_meta = [], []

    # Handle any leftover batch
    if batch_texts:
        vectors = embed_batch(batch_texts)
        for meta, vector in zip(batch_meta, vectors):
            meta["embedding"] = vector
            all_embeddings.append(meta)

    print(f"✅ {company_name}: Embedded {len(all_embeddings)} items total.")
    return all_embeddings

# --- Run for both Firestore DBs ---
dev_embeddings = fetch_and_embed(db_dev, fields_to_embed_dev, "Dev")
internal_embeddings = fetch_and_embed(db_internal, fields_to_embed_internal, "Internal")

# --- Save JSON outputs ---
with open("vector_db/dev_fields_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(dev_embeddings, f, ensure_ascii=False, indent=2)

with open("vector_db/internal_fields_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(internal_embeddings, f, ensure_ascii=False, indent=2)

print("🔥 All embeddings created and saved successfully!")
