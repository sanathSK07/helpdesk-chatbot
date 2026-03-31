# 🤖 IT Helpdesk RAG Chatbot

I built a Retrieval-Augmented Generation (RAG) chatbot that answers IT support questions by searching through enterprise documentation using vector similarity search — the same architecture behind ChatGPT plugins, Microsoft Copilot, and every modern enterprise AI assistant.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Database-green)
![RAG](https://img.shields.io/badge/RAG-Retrieval_Augmented_Generation-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red)

## 🎯 What It Does

IT help desks handle thousands of repetitive questions daily — "How do I reset my password?", "VPN won't connect", "How do I add a printer?" Most answers already exist in documentation, but employees can't find them quickly.

My chatbot solves this by searching a knowledge base using **semantic similarity** (understanding meaning, not just matching keywords), retrieving the most relevant documentation, and presenting it as a clear answer with source citations.

## 🏗️ How RAG Works

```
User asks: "My internet isn't working"
        ↓
Sentence-Transformers converts question → 384-dim vector
        ↓
ChromaDB finds nearest document vectors (semantic search)
        ↓
Top 3 relevant docs retrieved (VPN guide, WiFi setup, etc.)
        ↓
(Optional) LLM generates a polished answer using retrieved context
        ↓
User gets accurate, sourced answer — no hallucination
```

**Why RAG instead of fine-tuning?**
Fine-tuning is expensive, requires retraining when docs change, and can hallucinate. RAG retrieves real documents at query time, so answers are always grounded in source material and the knowledge base can be updated without any retraining.

## 🔬 Key Technical Decisions

**Why semantic search over keyword search?**
If a user asks "my internet isn't working", keyword search won't find a document titled "VPN Troubleshooting" because the words don't match. But semantic search understands that "internet not working" is related to "VPN troubleshooting" because their vector embeddings are close in meaning-space.

**Why all-MiniLM-L6-v2 for embeddings?**
It's a lightweight model (90MB) that creates quality 384-dimensional embeddings. It offers a good balance of speed and semantic accuracy — fast enough for real-time search, accurate enough for document retrieval. I didn't need a larger model because my knowledge base is domain-specific (IT support), not open-domain.

**Why ChromaDB?**
It runs locally with zero infrastructure setup, supports persistent storage (saves to disk), and has a simple Python API. Perfect for development and demos. In production, I'd migrate to a managed solution like Pinecone for scale.

**Why document chunking with overlap?**
A 500-word VPN article covers setup, troubleshooting, and Mac-specific issues. If someone asks about Mac VPN, I want to retrieve only the relevant paragraph — not the whole article. I split documents into ~300-word chunks with 50-word overlap so sentences at chunk boundaries aren't lost.

## 📊 Knowledge Base

| Category | Topics | Documents |
|----------|--------|-----------|
| Network | VPN setup, WiFi configuration | 2 |
| Account | Password reset, MFA, account recovery | 1 |
| Communication | Email setup, Teams meetings | 2 |
| Hardware | Printers, laptop performance | 2 |
| Software | Installation requests, approved apps | 1 |
| Security | Phishing, data protection, incident reporting | 1 |
| Onboarding | New employee IT checklist | 1 |

**10 documents → chunked → vectorized → searchable by meaning**

## 🛠️ Tech Stack

- **Vector Database:** ChromaDB (persistent local storage)
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`, 384 dimensions)
- **Frontend:** Streamlit (chat interface with source display)
- **LLM (Optional):** Anthropic Claude API for polished responses
- **Language:** Python

## 📁 Project Structure

```
helpdesk-chatbot/
├── app.py                      # Streamlit RAG chatbot interface
├── knowledge_base.py           # 10 IT helpdesk articles
├── 02_build_vectorstore.py     # Chunks docs, generates embeddings, stores in ChromaDB
├── requirements.txt            # Python dependencies
├── db/                         # ChromaDB persistent storage (generated)
│   └── config.json             # System configuration
└── README.md
```

## ⚡ Run It Yourself

```bash
git clone https://github.com/sanathSK07/helpdesk-chatbot.git
cd helpdesk-chatbot
pip install -r requirements.txt

# Build the vector store (one-time setup — downloads embedding model ~90MB)
python3 02_build_vectorstore.py

# Launch the chatbot
streamlit run app.py
```

**Two modes:**
- **Without API key (default):** Searches and returns relevant documentation directly
- **With Anthropic API key:** Full RAG — retrieves docs + generates polished LLM responses

## 💡 What I'd Improve Next

- Add more documents to the knowledge base (50+ articles)
- Implement conversation memory so follow-up questions have context
- Add a feedback loop where users rate answers to improve retrieval
- Implement hybrid search (vector + keyword) for better recall
- Deploy with a production vector database like Pinecone

## 📬 Contact

**Sanath** — York University, BA Information Technology

- GitHub: [sanathSK07](https://github.com/sanathSK07)
- LinkedIn: [sanath-kamaraj](https://linkedin.com/in/sanath-kamaraj)
- Email: Sanathkamaraj66@gmail.com

---

*⚠️ Portfolio project for educational purposes. Not connected to a real IT system.*
