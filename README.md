# FiNancy: GenAI based Financial Reports and Document Analyst

An **Automated Research Agent** built using **Retrieval-Augmented Generation (RAG)** that connects **live web data** with **Large Language Models** to answer questions using **news published minutes ago** — not stale training data.

This system acts as a **bridge between real-time information and generative AI**, ensuring answers are **grounded, factual, and source-aware**.

---

## 🚀 Key Features

- 🔎 **Live Web Research** using DuckDuckGo
- 🧠 **RAG Architecture** to prevent hallucinations
- ⚡ **Semantic Search** with FAISS
- 💾 **Persistent Memory** (no re-scraping on restart)
- 🌐 **Interactive UI** via Streamlit
- 🤖 **Powered by Google Gemini 2.5 Flash**

---

## 🏗️ System Architecture

The project is built on **four core pillars**:

| Component | Technology | Role |
|---------|-----------|------|
| **Interface** | Streamlit | Web dashboard, topic input, debug logs |
| **Orchestration** | LangChain | Connects tools, loaders, embeddings, and LLM |
| **Memory / Storage** | FAISS + Pickle | Vector similarity search & persistent storage |
| **LLM (Brain)** | Google Gemini 2.5 Flash | Reads retrieved data & generates answers |

---

## 🧬 How It Works (RAG Pipeline)

The agent follows a **4-stage pipeline** that transforms a user query into a **grounded conversational response**.

---

### 1️⃣ Automated Research (Discovery)

- Uses **DuckDuckGo Search Tool**
- Fetches top web snippets for the given topic
- Applies **custom Regex filtering** to extract the **top 2 clean URLs**
- Ensures only **high-relevance primary news sources** are used

📌 *Why?*  
Limits noise and improves factual precision.

---

### 2️⃣ Document Ingestion (Scraping & Processing)

- Uses `UnstructuredURLLoader` to scrape article text
- Applies **RecursiveCharacterTextSplitter**

**Chunking Strategy:**
- Chunk size: **1000 characters**
- Overlap: **200 characters**

📌 *Why overlap?*  
Preserves sentence continuity across chunks and prevents context loss.

---

### 3️⃣ Vectorization (Semantic Indexing)

This is where **AI-powered search** happens.

- **Embedding Model:** `all-MiniLM-L6-v2` (HuggingFace)
- Each text chunk → **numerical vector**
- Stored in **FAISS** for ultra-fast similarity search

📌 *Result:*  
Semantic understanding instead of keyword matching.

---

### 4️⃣ Retrieval & Answer Generation

When the user asks a question:

1. Question → converted into a vector
2. FAISS retrieves the **most relevant chunks**
3. Retrieved chunks + question → sent to **Gemini**
4. Gemini generates an answer **only using retrieved sources**

✅ Prevents hallucinations  
✅ Answers are grounded in real data  
✅ Sources can be traced back

---

## 💾 Persistence & Memory

- FAISS index is saved locally using `pickle.dump()`
- Stored as a `.pkl` file on disk
- On app restart:
  - Index is **reloaded**
  - Embedding function is **re-bound manually**

📌 *Why this matters?*  
Solves a common FAISS bug where loaded indexes lose search capability.

---

## 🔐 Authentication Strategy

- Bypasses **Google Application Default Credentials (ADC)**
- Explicitly passes `google_api_key` to the Gemini constructor

✅ Works on any local machine  
✅ No Google Cloud setup required  
✅ Developer-friendly

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **FAISS**
- **HuggingFace Embeddings**
- **Google Gemini 2.5 Flash**
- **DuckDuckGo Search**
- **Pickle**

---

## 📌 Use Cases

- Real-time news research
- Market & finance analysis
- Academic literature scanning
- Fact-checked GenAI chatbots
- Enterprise RAG systems

---

## 📈 Why This Project Stands Out

- Implements **true RAG**, not prompt stuffing
- Uses **live web data**, not static PDFs
- Handles **persistence and cold reloads**
- Production-oriented architecture
- Resume-ready GenAI system design

---

<img width="959" height="472" alt="image" src="https://github.com/user-attachments/assets/703c63ae-f8b4-4e31-8de1-091a016c1a4d" />
<img width="943" height="352" alt="image" src="https://github.com/user-attachments/assets/e6d1f405-3ddb-4b3a-8766-91b4522a01c6" />
<img width="870" height="389" alt="image" src="https://github.com/user-attachments/assets/4ff043e7-188c-4989-9151-0ee30b719b90" />
<img width="842" height="359" alt="image" src="https://github.com/user-attachments/assets/580baec5-736d-42e4-a4d0-3154fc9e3e73" />




## 📜 License

MIT License

---

## 👤 Author

**Anandapadmanabhan B**  
*GenAI | RAG Systems | Full-Stack AI Engineering*

---

⭐ If you find this useful, consider starring the repo!
