# 📚 gen-ai

A **Generative AI project** powered by **LangChain**, **Retrieval-Augmented Generation (RAG)**, and a custom chatbot that combines retrievers with MCP-based processing.

---

## 🎬 GenAI YouTube Script Generator

This tool is an AI-powered assistant that generates **YouTube video scripts** based on user-defined topics. It leverages the power of **LangChain**, **HuggingFace embeddings**, and **Groq's LLaMA 3.3-70B model** to create compelling video content in seconds.

---

## 🚀 Features

- 🔍 **RAG-based document retrieval** using PDFs and Chroma vector store
- 🤖 **Interactive chatbot interface** for entering YouTube topics
- 🧠 **Automated generation** of:
  - Video titles
  - Content segments
  - Complete scripts
- 💾 **Saves the script** as a `.txt` file
- 🌐 Uses `sentence-transformers` for embeddings and **Groq’s LLaMA-3** for high-quality outputs

---

## 🛠️ Tech Stack

- **LangChain**
- **HuggingFace Transformers** (`all-MiniLM-L6-v2`)
- **Groq’s LLaMA 3.3-70B**
- **Chroma Vector DB**
- **Python 3.10+**
- **dotenv** for API key and environment variable management

---

## 🧩 Project Structure

```
gen-ai/
├── data/         # Folder containing input PDF documents
├── db/           # Persistent ChromaDB vector store
├── chain.py      # Main script for YouTube script generation
├── rag.py        # Builds the retriever from PDFs using LangChain
├── .env          # Stores environment variables like API keys
```

---

## 💡 How It Works

1. **`rag.py`**:
   - Loads PDFs from the `data/` folder
   - Splits and embeds the text using HuggingFace
   - Stores vectors in a Chroma DB

2. **`chain.py`**:
   - Loads the retriever
   - Defines a 3-step generation chain using LLMs:
     1. Generate a **YouTube title** from the user topic
     2. Generate 10 **content segments**
     3. Generate a full **script** based on the segments

3. **User Interaction**:
   - Enter any topic via the terminal
   - The system generates and saves a detailed video script
