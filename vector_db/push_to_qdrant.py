# vector_db/push_to_qdrant.py
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_connection import qdrant_client  # your initialized client

# Config: collection names & embedding files
collections_config = [
    {
        "name": "dev_fields",
        "embeddings_file": "vector_db/dev_fields_embeddings.json",
        "company_id": "dev"
    },
    {
        "name": "internal_fields",
        "embeddings_file": "vector_db/internal_fields_embeddings.json",
        "company_id": "internal"
    }
]

VECTOR_SIZE = 384  # must match your embedding model

for col in collections_config:
    # Ensure collection exists
    if not qdrant_client.collection_exists(col["name"]):
        qdrant_client.create_collection(
            collection_name=col["name"],
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
        )
        print(f"✅ Collection '{col['name']}' created.")
    else:
        print(f"ℹ️ Collection '{col['name']}' already exists. New points will be upserted.")

    # Load embeddings
    with open(col["embeddings_file"], "r", encoding="utf-8") as f:
        embeddings = json.load(f)

    points = []
    for item in embeddings:
        # Generate stable ID using collection + text snippet
        text_snippet = item.get("text", "")[:50]  # first 50 chars
        point_id = abs(hash(f"{col['name']}_{hash(text_snippet)}"))

        payload = {
            "company_id": col["company_id"],
            "text": item.get("text", "")
        }
        if "collection" in item:
            payload["source_collection"] = item["collection"]
        if "field_name" in item:
            payload["field_name"] = item["field_name"]

        points.append(
            models.PointStruct(
                id=point_id,
                vector=item["embedding"],
                payload=payload
            )
        )

    # Batch upsert for efficiency
    BATCH_SIZE = 64
    for i in range(0, len(points), BATCH_SIZE):
        batch = points[i:i + BATCH_SIZE]
        qdrant_client.upsert(collection_name=col["name"], points=batch)

    print(f"✅ Uploaded {len(points)} embeddings to '{col['name']}'!\n")
