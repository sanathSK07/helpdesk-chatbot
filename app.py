# ============================================================
# IT Helpdesk RAG Chatbot - Web Application
# Author: Sanath | York University
# ============================================================
# I built this chatbot using the RAG (Retrieval-Augmented
# Generation) architecture — the same approach behind ChatGPT
# plugins and Microsoft Copilot. When a user asks a question,
# my system searches a vector database for relevant documents,
# then generates an answer grounded in those sources. This
# prevents hallucination and ensures every answer is sourced.
# ============================================================

import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import json
import time
import os

st.set_page_config(page_title="IT Helpdesk AI Assistant", page_icon="🤖", layout="wide")

@st.cache_resource
def load_resources():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./db")
    collection = client.get_collection("it_helpdesk")
    config = json.load(open("db/config.json"))
    return model, collection, config

embedding_model, collection, config = load_resources()

st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; background: linear-gradient(90deg, #1e3a5f, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .sub-header { text-align: center; color: #6b7280; font-size: 1rem; margin-top: -10px; margin-bottom: 20px; }
    .source-card { background: #f8fafc; border-radius: 8px; padding: 12px 16px; margin: 8px 0; border-left: 3px solid #2563eb; }
    .similarity-badge { background: #dbeafe; color: #1d4ed8; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
    .category-badge { background: #f0fdf4; color: #15803d; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; }
    .stButton > button { width: 100%; background: linear-gradient(90deg, #1e3a5f, #2563eb); color: white; border: none; padding: 10px; font-size: 1rem; font-weight: 600; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🤖 IT Helpdesk AI Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask me anything about IT support — powered by RAG (Retrieval-Augmented Generation)</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔧 System Info")
    st.metric("Knowledge Base", f"{config['total_documents']} docs")
    st.metric("Indexed Chunks", f"{config['total_chunks']}")
    st.metric("Embedding Model", config['embedding_model'])
    st.metric("Vector Dimensions", config['embedding_dimensions'])
    st.divider()
    st.markdown("### ⚙️ Search Settings")
    num_results = st.slider("Results to retrieve", 1, 5, 3)
    show_sources = st.checkbox("Show source documents", value=True)
    st.divider()
    # I added optional API key support — the app works without it using direct retrieval,
    # but with a key it generates polished LLM responses
    st.markdown("### 🔑 AI Response (Optional)")
    api_key = st.text_input("Anthropic API Key", type="password", help="Optional: enables AI-generated responses. Without it, I show retrieved documents directly.")
    st.divider()
    st.markdown("### 🎯 How My RAG Pipeline Works")
    st.markdown("""
    1. **Retrieve**: Question → vector → ChromaDB similarity search
    2. **Augment**: Top documents combined with the question
    3. **Generate**: LLM crafts answer using retrieved context
    """)
    st.divider()
    st.markdown("<div style='text-align:center;color:#9ca3af;font-size:0.8rem;'>Built by Sanath | York University<br>ChromaDB • Sentence-Transformers • Streamlit</div>", unsafe_allow_html=True)


# My RAG pipeline functions
def retrieve_context(query, n_results=3):
    """Step 1: RETRIEVE — search ChromaDB for relevant document chunks."""
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=n_results)
    retrieved = []
    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]
        similarity = round(1 / (1 + distance), 3)
        retrieved.append({
            "text": results["documents"][0][i],
            "title": results["metadatas"][0][i]["title"],
            "category": results["metadatas"][0][i]["category"],
            "similarity": similarity,
            "id": results["ids"][0][i]
        })
    return retrieved

def build_prompt(query, context_docs):
    """Step 2: AUGMENT — combine retrieved docs with the user question into a prompt."""
    context_text = "\n\n---\n\n".join([f"Source: {doc['title']} [{doc['category']}]\n{doc['text']}" for doc in context_docs])
    return f"""You are an IT Helpdesk AI Assistant. Answer the user's question using ONLY the context provided below. Be helpful, clear, and concise. If the context doesn't contain enough information, say so.

CONTEXT FROM KNOWLEDGE BASE:
{context_text}

USER QUESTION: {query}

INSTRUCTIONS:
- Answer based ONLY on the provided context
- Use bullet points for step-by-step instructions
- Include URLs or contact info if mentioned in the context
- If unsure, say "I couldn't find specific information about that. Please contact IT Help Desk at ext. 5555."

ANSWER:"""

def generate_response_with_api(prompt, api_key):
    """Step 3: GENERATE — use Claude API for polished responses."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=1024, messages=[{"role": "user", "content": prompt}])
        return message.content[0].text
    except Exception as e:
        return f"API Error: {str(e)}"

def generate_response_local(query, context_docs):
    """Fallback response using retrieved documents directly (no API needed)."""
    if not context_docs or context_docs[0]["similarity"] < 0.3:
        return "I couldn't find relevant information in our knowledge base. Please contact IT Help Desk at ext. 5555 or helpdesk@company.com."
    best_doc = context_docs[0]
    response = f"Based on our **{best_doc['title']}** documentation:\n\n{best_doc['text']}"
    if len(context_docs) > 1 and context_docs[1]["similarity"] > 0.4:
        response += f"\n\n---\n\nAdditional info from **{context_docs[1]['title']}**:\n\n{context_docs[1]['text']}"
    response += "\n\n---\n*Need more help? Contact IT Help Desk at ext. 5555 or helpdesk@company.com.*"
    return response


# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# I added suggested questions to help users get started
if len(st.session_state.messages) == 0:
    st.markdown("### 💡 Try asking:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 How do I reset my password?"): st.session_state.pending_query = "How do I reset my password?"; st.rerun()
        if st.button("🌐 VPN won't connect, what should I do?"): st.session_state.pending_query = "VPN won't connect, what should I do?"; st.rerun()
        if st.button("🖨️ How do I add a printer?"): st.session_state.pending_query = "How do I add a printer?"; st.rerun()
    with col2:
        if st.button("💻 My laptop is running slowly"): st.session_state.pending_query = "My laptop is running slowly"; st.rerun()
        if st.button("📧 How to set up email on my phone?"): st.session_state.pending_query = "How to set up email on my phone?"; st.rerun()
        if st.button("🆕 I'm new, what do I set up?"): st.session_state.pending_query = "I'm a new employee, what do I need to set up?"; st.rerun()

query = st.session_state.pop("pending_query", None) or st.chat_input("Ask me an IT question...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching knowledge base..."):
            start = time.time()
            context_docs = retrieve_context(query, n_results=num_results)
            retrieval_time = time.time() - start

        with st.spinner("🤖 Generating response..."):
            start = time.time()
            if api_key:
                response = generate_response_with_api(build_prompt(query, context_docs), api_key)
            else:
                response = generate_response_local(query, context_docs)
            gen_time = time.time() - start

        st.markdown(response)
        c1, c2, c3 = st.columns(3)
        c1.caption(f"⚡ Retrieval: {retrieval_time:.2f}s")
        c2.caption(f"🤖 Generation: {gen_time:.2f}s")
        c3.caption(f"📄 Sources: {len(context_docs)}")

        if show_sources:
            with st.expander("📚 Source Documents"):
                for src in context_docs:
                    st.markdown(f'<div class="source-card"><strong>{src["title"]}</strong> <span class="category-badge">{src["category"]}</span> <span class="similarity-badge">{src["similarity"]*100:.1f}% match</span><p style="font-size:0.85rem;color:#4b5563;margin-top:8px;">{src["text"][:300]}...</p></div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response, "sources": context_docs})

st.markdown("---")
st.markdown("<div style='text-align:center;color:#9ca3af;padding:10px;'><p><strong>IT Helpdesk AI Assistant</strong> | RAG Architecture</p><p>ChromaDB • Sentence-Transformers • Streamlit</p><p>Built by <strong>Sanath</strong> | York University | 2026</p></div>", unsafe_allow_html=True)
