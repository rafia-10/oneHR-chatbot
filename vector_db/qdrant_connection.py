import os
from qdrant_client import QdrantClient

# Fetch credentials from environment
api_key = os.environ.get("QDRANT_API_KEY")
url = os.environ.get("QDRANT_URL")

# Connect to Qdrant
qdrant_client = QdrantClient(url=url, api_key=api_key)

# Test connection
try:
    collections = qdrant_client.get_collections()
    print("✅ Connected to Qdrant! Available collections:", [c.name for c in collections.collections])
except Exception as e:
    print(f"❌ Failed to connect: {e}")
