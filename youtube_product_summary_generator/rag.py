# Optional: Create and activate virtual environment (uncomment if needed)
# python -m venv venv
# .\venv\Scripts\activate

import os
import warnings
warnings.filterwarnings("ignore", message="Ignoring wrong pointing object")

# Environment variables (e.g., API keys)
from dotenv import load_dotenv
load_dotenv()

# LangChain + PDF processing
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma  # type: ignore # ✅ Only use the updated Chroma
from langchain.chains import RetrievalQA

# Initialize HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

# Directory to persist/load Chroma DB
db_path = "db"

# Load or create Chroma vector store
if os.path.exists(db_path):
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
else:
    loader = PyPDFDirectoryLoader("data")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(docs)

    db = Chroma.from_documents(texts, embedding_function=embeddings, persist_directory=db_path)
    db.persist()
    print("✅ Created and saved new Chroma index.")

# Set up retriever
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
