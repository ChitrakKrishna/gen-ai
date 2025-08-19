# 🚀 gen-ai

A collection of Generative AI projects built with **LangChain**, **Retrieval-Augmented Generation (RAG)**, and **custom chatbots** powered by **Groq LLMs, HuggingFace embeddings, and modular retrievers**.

---

## 📺 GenAI YouTube Script Generator

An **AI-powered YouTube script assistant** that generates titles, content segments, and full scripts using RAG and Groq’s LLaMA models.

### ✨ Features
- 🔍 **RAG-based document understanding** with PDFs + Chroma Vector DB  
- 🤖 **Chat interface** for entering YouTube topics  
- 🧠 **Automatic generation** of titles, segments & scripts  
- 💾 **Saves scripts** to `.txt` files  
- 🌐 **High-quality responses** via Groq’s `llama-3-70b`  

### 🛠 Tech Stack
- LangChain  
- HuggingFace Embeddings (`all-MiniLM-L6-v2`)  
- Groq LLaMA 3.3-70B  
- Chroma Vector DB  
- Python 3.10+  

### 📂 Project Structure
gen-ai-youtube/
├── data/ # Input PDF documents
├── db/ # ChromaDB storage
├── chain.py # Main script for generation
├── rag.py # Retriever builder
└── .env # API keys and configs





### ⚙️ How It Works
1. `rag.py` → Loads PDFs, embeds, stores vectors in ChromaDB  
2. `chain.py` → Defines 3-step chain:  
   - Generate YouTube **title** from topic  
   - Generate **10 segments** from title  
   - Generate full **script** from segments  

---

## 🔐 RBAC Chatbot (Role-Based Access Control Chatbot)

A **FastAPI chatbot** with RBAC to authenticate users and provide **department-specific answers** powered by LangChain + Groq.

### ✨ Features
- 🔑 **RBAC Authentication** (email + employee ID)  
- 🏢 **Department-based Q&A** (HR, Finance, Marketing, Engineering, etc.)  
- 💬 **Chatbot with fallback responses**  
- ⚡ **FastAPI backend** with `/login` & `/chat` endpoints  
- 🧩 **Modular retrievers** for each department  

### 🛠 Tech Stack
- FastAPI  
- LangChain  
- Groq LLMs  
- CSV-based HR dataset  

### 📂 Project Structure
rbac-chatbot/
├── admin.py # HR data authentication & dept. retrieval
├── main.py # FastAPI server
├── retrieval.py # Chat logic + retrievers
├── requirements.txt # Dependencies
└── DS-RPC-01/
├── data/hr/hr_data.csv # HR dataset
└── metadata.txt # Chatbot instructions





---

## 📰 Newspaper RAG Chatbot

A **RAG-based chatbot** that fetches web content, stores it in FAISS, and answers queries with context-aware responses.

### ✨ Features
- 🌐 **Web data loader** (fetch content from URLs)  
- 🔎 **FAISS vector store** for retrieval  
- 🧠 **Dual LLMs**:  
  - HuggingFace Llama-3.1-8B-Instruct  
  - Groq LLaMA 3.3-70B-Versatile  
- 💬 **Conversational Q&A** with concise outputs  
- ⚡ **RAG pipeline** for context-aware answers  

### 🛠 Tech Stack
- LangChain  
- HuggingFace Embeddings  
- Groq LLMs  
- FAISS Vector DB  

### 📂 Project Structure
newspaper-chatbot/
├── rag.py # Load URLs + build FAISS retriever
├── retrieval.py # Chatbot logic
├── requirements.txt # Dependencies
├── faiss_index/ # Saved FAISS DB
└── .env # API keys
