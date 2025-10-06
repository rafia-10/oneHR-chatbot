import os 
from qdrant_client import QdrantClient

api_key = os.environ.get("QDRANT_API_KEY")
url = os.environ.get("QDRANT_URL")

# 🔑 Connect to Qdrant
qdrant_client = QdrantClient(url=url, api_key=api_key)

# ✅ Ensure index exists
try:
    qdrant_client.create_payload_index(
        collection_name="hr_documents",
        field_name="company_id",
        field_schema="keyword"
    )
    print("✅ Index created for company_id")
except Exception as e:
    print(f"⚠️ Skipped index creation (maybe it already exists): {e}")

# ✅ Test connection
try:
    collections = qdrant_client.get_collections()
    print("Successfully connected to Qdrant! Available collections:", [c.name for c in collections.collections])
except Exception as e:
    print(f"❌ Failed to connect: {e}")
