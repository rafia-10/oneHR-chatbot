import json
import re
def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# Load your RAG-ready file
with open("rag_ready.json", "r", encoding="utf-8") as f:
    rag_docs = json.load(f)

rag_chunks = []

for doc in rag_docs:
    text = doc.get("text", "")
    chunks = chunk_text(text)
    match = re.search(r"company:\s*(\S+)", text)
    company_id = match.group(1) if match else "no-company"
    
    for i, chunk in enumerate(chunks):
        rag_chunks.append({
            "collection": doc.get("collection", "unknown"),
            "id": f"{doc.get('id', 'unknown')}_chunk{i}",
            "companyId": company_id,
            "text": chunk
        })
  


# Save chunked output
with open("rag_chunks.json", "w", encoding="utf-8") as f:
    json.dump(rag_chunks, f, ensure_ascii=False, indent=2)

print(f"Chunked {len(rag_docs)} docs into {len(rag_chunks)} chunks ✅")



