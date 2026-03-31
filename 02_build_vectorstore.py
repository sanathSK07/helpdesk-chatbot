# ============================================================
# Build Vector Store for RAG Pipeline
# Author: Sanath | York University
# ============================================================
# I built this script to convert my IT knowledge base articles
# into vector embeddings and store them in ChromaDB. This is the
# "Retrieval" part of RAG — it enables semantic search so the
# chatbot can find relevant docs based on meaning, not just keywords.
# ============================================================

import chromadb
from sentence_transformers import SentenceTransformer
from knowledge_base import KNOWLEDGE_BASE
import json

print("=" * 60)
print("🔧 BUILDING VECTOR STORE")
print("=" * 60)

# I chose all-MiniLM-L6-v2 because it's lightweight (90MB), fast,
# and creates quality 384-dim embeddings — good balance for a portfolio project
print("\n📦 Loading embedding model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("   ✅ Model loaded!")

# I chunk documents into smaller pieces so the retriever can find
# the specific paragraph that answers a question, not the entire article
def chunk_document(doc, chunk_size=300, overlap=50):
    """Split a document into overlapping chunks."""
    content = doc["content"]
    words = content.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk_text = " ".join(words[i:i + chunk_size])
        if len(chunk_text.strip()) > 50:
            chunks.append({
                "id": f"{doc['id']}-chunk-{len(chunks)}",
                "text": chunk_text,
                "title": doc["title"],
                "category": doc["category"],
                "source_id": doc["id"]
            })
    return chunks

print("\n✂️  Chunking documents...")
all_chunks = []
for doc in KNOWLEDGE_BASE:
    chunks = chunk_document(doc)
    all_chunks.extend(chunks)
    print(f"   {doc['title']}: {len(chunks)} chunk(s)")
print(f"\n   Total chunks: {len(all_chunks)}")

# I use ChromaDB's persistent client so the vectors save to disk
# and my Streamlit app can load them without rebuilding every time
print("\n💾 Creating ChromaDB collection...")
client = chromadb.PersistentClient(path="./db")
try:
    client.delete_collection("it_helpdesk")
except:
    pass

collection = client.create_collection(
    name="it_helpdesk",
    metadata={"description": "IT Helpdesk Knowledge Base"}
)

# Generate embeddings for all chunks at once (batch processing is faster)
print("\n🧠 Generating embeddings and storing vectors...")
texts = [chunk["text"] for chunk in all_chunks]
embeddings = model.encode(texts, show_progress_bar=True)

collection.add(
    ids=[chunk["id"] for chunk in all_chunks],
    embeddings=embeddings.tolist(),
    documents=texts,
    metadatas=[{"title": chunk["title"], "category": chunk["category"], "source_id": chunk["source_id"]} for chunk in all_chunks]
)
print(f"\n   ✅ Stored {len(all_chunks)} chunks in ChromaDB!")

# Testing to make sure semantic search works correctly
print("\n🔍 Testing vector search...")
test_queries = [
    "How do I connect to the VPN?",
    "I forgot my password",
    "My laptop is slow",
    "How do I set up my email on my phone?",
    "Is it safe to click this link?"
]

for query in test_queries:
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=2)
    print(f"\n   Q: \"{query}\"")
    for i, (doc, score) in enumerate(zip(results["metadatas"][0], results["distances"][0])):
        similarity = round(1 / (1 + score), 2)
        print(f"      #{i+1}: [{doc['category']}] {doc['title']} (similarity: {similarity})")

json.dump({
    "total_documents": len(KNOWLEDGE_BASE), "total_chunks": len(all_chunks),
    "embedding_model": "all-MiniLM-L6-v2", "embedding_dimensions": 384,
    "chunk_size": 300, "chunk_overlap": 50
}, open("db/config.json", "w"), indent=2)

print(f"\n🎉 VECTOR STORE BUILT — {len(KNOWLEDGE_BASE)} docs → {len(all_chunks)} chunks → {len(all_chunks)} vectors")
