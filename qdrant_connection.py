import os 
from qdrant_client import QdrantClient

api_key = os.environ.get('QDRANT_API_KEY')
url= os.environ.get('QDRANT_URL')
# 🔑 Connect to Qdrant
qdrant_client = QdrantClient(
    url= url, 
    api_key= api_key,


)
try:
    qdrant_client.get_collections()
    print("Successfully connected to Qdrant!")
except Exception as e:
    print(f"Failed to connect to Qdrant: {e}")