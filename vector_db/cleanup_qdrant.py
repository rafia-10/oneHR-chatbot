from qdrant_connection import qdrant_client

# 🚨 Option 1: delete the whole collection
qdrant_client.delete_collection("onehr_dev")
