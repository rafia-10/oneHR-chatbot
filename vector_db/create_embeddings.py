import os
import json
from firestore_utils import fetch_documents
from text_utils import extract_text, chunk_text
from embedding_model import embed_batch
from config import BATCH_SIZE, OUTPUT_DIR
from firebase_connect import db_dev, db_internal

def fetch_and_embed(db, company_name):
    all_embeddings = []

    for coll_ref in db.collections():
        coll_name = coll_ref.id
        print(f"📦 {company_name} - processing collection: {coll_name}")

        batch_texts, batch_meta = [], []
        for doc in fetch_documents(db, coll_name):
            texts = extract_text(doc)
            for t in texts:
                for chunk_index, chunk in enumerate(chunk_text(t)):
                    batch_texts.append(chunk)
                    batch_meta.append({
                        "collection": coll_name,
                        "doc_id": doc.get('id', None),
                        "chunk_index": chunk_index,
                        "text": chunk
                    })

                    if len(batch_texts) >= BATCH_SIZE:
                        vectors = embed_batch(batch_texts)
                        for meta, vector in zip(batch_meta, vectors):
                            meta["embedding"] = vector
                            all_embeddings.append(meta)
                        batch_texts, batch_meta = [], []

        # leftover batch
        if batch_texts:
            vectors = embed_batch(batch_texts)
            for meta, vector in zip(batch_meta, vectors):
                meta["embedding"] = vector
                all_embeddings.append(meta)

        print(f"✅ {company_name} - embedded {len(all_embeddings)} items from {coll_name}")

    return all_embeddings

def save_embeddings(embeddings, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=2)


DB_MAPPING = {"Dev": db_dev, "Internal": db_internal}

for company_name, db in DB_MAPPING.items():
    embeddings = fetch_and_embed(db, company_name)
    path = os.path.join(OUTPUT_DIR, f"{company_name.lower()}_fields_embeddings.json")
    save_embeddings(embeddings, path)
    print(f"🔥 {company_name} embeddings saved to {path}")
