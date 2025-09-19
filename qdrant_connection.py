from google.colab import userdata
from qdrant_client import QdrantClient

api_key = userdata.get('QDRANT_API_KEY')
url= userdata.get('QDRANT_URL')
# 🔑 Connect to Qdrant
qdrant_client = QdrantClient(
    url= url, 
    api_key= api_key,
)
