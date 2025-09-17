import json
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models

# 🔑 Connect to Qdrant
qdrant_client = QdrantClient(
    url="https://6ac6eea9-e469-4661-8a71-5cd940dfb6a7.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Cm3DQ5g4E-Lo5N652FZ99RGI0ax1ex43lN-8ba7qGik",
)


# Load embeddings from JSON
with open("rag_embeddings.json", "r") as f:
    rag_embeddings = json.load(f)

# (Re)create collection – only run once unless you want to wipe/reset
qdrant_client.recreate_collection(
    collection_name="hr_documents",
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
)

# Prepare points
points = []
for item in rag_embeddings:
    points.append(
        models.PointStruct(
            id=str(uuid.uuid4()),   
            vector=item["embedding"],
            payload={
                "company_id": item["companyId"],   # 🔑 multi-tenant
                "collection": item["collection"],  # optional grouping
                "text": item.get("text", ""), 
                "orig_id": item["id"],
            }
        )
    )

# Upload to Qdrant
qdrant_client.upsert(
    collection_name="hr_documents",
    points=points
)

print(f"✅ Uploaded {len(points)} embeddings to Qdrant!")
