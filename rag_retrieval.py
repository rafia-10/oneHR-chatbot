import json
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_connection import qdrant_client   # ✅ reuse your connection
from query_embedding import embed_text


# --- Load the embedding model ---
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)



def get_user_company(user_id):
    """
    Fetch the companyId for the given user_id from rag_chunks.json
    user_id should match the '_id' field in rag_chunks.json
    """
    with open("rag_chunks.json", "r") as f:
        users = json.load(f)

    for user in users:
        if user.get("_id") == user_id:   # match applicant _id
            return user.get("companyId", None)
    return None


def retrieve_chunks(user_query, user_id, top_k=5):
    """
    Given a query + user_id:
    1. Embed the query
    2. Get companyId for multi-tenancy
    3. Search Qdrant for top_k relevant chunks
    """
    # Step 1: Embed query
    query_vector = embed_text(user_query)

    # Step 2: Get companyId for filtering
    user_company_id = get_user_company(user_id)
    if not user_company_id:
        raise ValueError(f"❌ No company found for user_id={user_id}")

    # Step 3: Query Qdrant
    search_results = qdrant_client.search(
        collection_name="hr_documents",
        query_vector=query_vector,
        limit=top_k,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="company_id",
                    match=models.MatchValue(value=user_company_id)
                )
            ]
        )
    )

    # Step 4: Extract text chunks
    chunks = [hit.payload.get("text", "") for hit in search_results]
    return chunks


# --- Example usage ---
if __name__ == "__main__":
    user_id = "P9AeXsZBe3DxNFnJLmCh"  # example applicant ID from rag_chunks.json
    user_question = "How many leave days does Kevin have?"

    chunks = retrieve_chunks(user_question, user_id, top_k=3)
    print("🔍 Retrieved Chunks:")
    for c in chunks:
        print("-", c[:200], "...")
