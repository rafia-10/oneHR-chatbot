import json
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_connection import qdrant_client

# Config: collection names & embeddings files
collections_config = [
    {
        "name": "dev_fields",
        "embeddings_file": "vector_db/dev_fields_embeddings.json",
        "company_id": "dev"  # multi-tenant identifier
    },
    {
        "name": "internal_fields",
        "embeddings_file": "vector_db/internal_fields_embeddings.json",
        "company_id": "internal"
    }
]

for col in collections_config:
    # Recreate collection (deletes old collection, so careful!)
    qdrant_client.recreate_collection(
        collection_name=col["name"],
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
    )
    print(f"✅ Collection '{col['name']}' created/reset.")

    # Load embeddings
    with open(col["embeddings_file"], "r") as f:
        embeddings = json.load(f)

    # Prepare points
    points = [
        models.PointStruct(
            id=str(uuid.uuid4()),
            vector=item["embedding"],
            payload={
                "company_id": col["company_id"],
                "field_name": item["field_name"]
            }
        ) for item in embeddings
    ]

    # Upload to Qdrant
    qdrant_client.upsert(collection_name=col["name"], points=points)
    print(f"✅ Uploaded {len(points)} embeddings to '{col['name']}'!\n")
