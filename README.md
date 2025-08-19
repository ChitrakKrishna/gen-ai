# \# gen-ai

# A Generative AI project using LangChain, Retrieval-Augmented Generation (RAG), and a custom chatbot powered by retrievers and MCP-based processing.

# 

# 

# 📺 GenAI YouTube Script Generator : 

# This project is an AI-powered YouTube script generation assistant built using LangChain, HuggingFace embeddings, and Retrieval-Augmented Generation (RAG) with the ChatGroq LLM.

# 

# 🚀 Features

# 🔍 RAG-based document understanding using PDFs and Chroma vector store

# 

# 🤖 Chat interface for entering YouTube topics

# 

# 🧠 Automatic title, segment, and script generation for videos

# 

# 💾 Saves the generated script to a .txt file

# 

# 🌐 Uses sentence-transformers for embeddings and Groq's llama-3-70b for high-quality responses

# 

# 🛠️ Tech Stack

# >> LangChain

# 

# >> HuggingFace Embeddings (all-MiniLM-L6-v2)

# 

# >> Groq's LLaMA 3.3-70B model

# 

# >> Chroma Vector DB

# 

# >> .env for secret management

# 

# >> Python 3.10+

# 

# 🧩 Project Structure

# 📁 data/                # Folder for input PDF documents

# 📁 db/                  # ChromaDB storage folder

# 📄 chain.py             # Main script for generating YouTube scripts

# 📄 rag.py               # Builds retriever using PDF data

# .env                    # Environment variables

# 

# 

# 💡 How it Works

# rag.py loads PDF data, splits and embeds it, and stores it in a Chroma vector database.

# 

# chain.py loads this retriever and defines a 3-step LLM chain:

# 

# 🔹 Generate a YouTube title from a topic

# 

# 🔹 Generate 10 content segments from the title

# 

# 🔹 Generate a detailed script from segments

# 

# You interactively enter topics and receive full YouTube-ready scripts.





RBAC-Chatbot (Role-Based Access Control Chatbot)

This project is a FastAPI-based chatbot with Role-Based Access Control (RBAC).
It authenticates users via their email and employee ID, fetches their department, and then provides department-specific responses powered by LangChain and Groq LLMs.

🚀 Features

🔐 Role-Based Access Control (RBAC): Authenticate users via email & employee ID from HR data.

💬 Chatbot: Department-specific Q&A with fallback to general responses.

⚡ FastAPI Backend: Simple APIs for login and chat.

🤖 LLM Integration: Uses Groq models with LangChain retrievers.

🗂 Modular Retrievers: Supports multiple departments (HR, Finance, Marketing, Engineering, etc.).

📂 Project Structure
.
├── admin.py          # Handles HR data authentication & department retrieval
├── main.py           # FastAPI server with /login and /chat endpoints
├── retrieval.py      # Chat logic, retrievers, LLM integration
├── requirements.txt  # Python dependencies
└── DS-RPC-01/
    ├── data/hr/hr_data.csv   # HR employee dataset
    └── metadata.txt          # Custom chatbot instructions



