import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd

# === Load CSV ===
df = pd.read_csv(r"DS-RPC-01\data\hr\hr_data.csv")

# === Create embeddings ===
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# === Paths ===
db_path = r'vector_dbs/hr'

# === Check if Chroma DB exists ===
if os.path.exists(db_path) and len(os.listdir(db_path)) > 0:
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    print("Loaded existing Chroma DB.")
else:
    # === Convert rows to text documents ===
    loader = DataFrameLoader(df, page_content_column="full_name")
    docs = loader.load()

    # === Split text (optional for long text) ===
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    chunks = text_splitter.split_documents(docs)

    # ✅ FIX: use `chunks` instead of `text_splitter` in `from_documents`
    db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_path)
    db.persist()
    print("Created and saved new Chroma DB.")

# === Create retriever ===
hr_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
print("Retriever is ready.")
