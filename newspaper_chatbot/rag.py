#!python -m venv venv
#!.\venv\Scripts\activate


# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Retrieve API keys
apicroq = os.getenv('ChatGroqAPIKey')
huggingface_api = os.getenv('APIKey')

# Import LLMs
from langchain_huggingface import HuggingFaceEndpoint
from langchain_groq import ChatGroq

llm_hf = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    temperature=0.7,
    token=huggingface_api  # type: ignore
)

llm = ChatGroq(
    api_key=apicroq,        # type: ignore
    model="llama-3.3-70b-versatile",
    temperature=0.9
)

# Load URLs
from langchain_community.document_loaders import UnstructuredURLLoader
urlLoader = UnstructuredURLLoader(
    urls=[
        "https://www.moneycontrol.com/news/business/banks/hdfc-bank-re-appoints-sanmoy-chakrabarti-as-chief-risk-officer-11259771.html",
        "https://www.moneycontrol.com/news/business/markets/market-corrects-post-rbi-ups-inflation-forecast-icrr-bet-on-these-top-10-rate-sensitive-stocks-ideas-11142611.html"
    ]
)

docs = urlLoader.load()

docs

# Text splitting
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)
print("Number of chunks created:", len(chunks))

# Create or Load FAISS index
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

db_path = "faiss_index"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})

if os.path.exists(db_path):
    vector_index = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS index loaded from disk.")
else:
    vector_index = FAISS.from_documents(chunks, embeddings)
    vector_index.save_local(db_path)
    print("✅ New FAISS index created and saved.")

# Create retriever
retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 2})
