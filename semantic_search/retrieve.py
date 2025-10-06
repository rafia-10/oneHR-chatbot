# retrieve.py
from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
from query_embedding import embed_text

# connect to Qdrant
qdrant_client = QdrantClient(
    url="https://6ac6eea9-e469-4661-8a71-5cd940dfb6a7.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Cm3DQ5g4E-Lo5N652FZ99RGI0ax1ex43lN-8ba7qGik",
)

def retrieve_chunks(question, top_k=3):
    query_vector = embed_text(question)
    search_result = qdrant_client.search(
        collection_name="hr_documents",
        query_vector=query_vector,
        limit=top_k
    )
    return [hit.payload["text"] for hit in search_result]
