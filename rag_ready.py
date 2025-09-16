import json

def flatten_doc(doc, parent_key=""):
    """Recursively flattens nested dicts/lists into key: value pairs."""
    items = []
    for k, v in doc.items():
        new_key = f"{parent_key}.{k}" if parent_key else k

        if isinstance(v, dict):
            items.extend(flatten_doc(v, new_key).items())
        elif isinstance(v, list):
            # flatten each item in list
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_doc(item, f"{new_key}[{i}]").items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, v))
    return dict(items)

def make_text(doc):
    """Convert flattened doc into a single text string for embeddings."""
    flat = flatten_doc(doc)
    parts = [f"{k}: {v}" for k, v in flat.items()]
    return "\n".join(parts)

# === MAIN ===
with open("all_collections.json", "r") as f:
    data = json.load(f)  # list of all docs from all collections

rag_chunks = []
for d in data:
    text = make_text(d)
    rag_chunks.append({
        "collection": d.get("_collection", "unknown"),
        "id": d.get("_id", "unknown"),
        "text": text
    })

# save to new file for embeddings
with open("rag_ready.json", "w") as f:
    json.dump(rag_chunks, f, indent=2)

print(f"Prepared {len(rag_chunks)} docs for RAG")
