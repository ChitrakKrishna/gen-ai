import os
import warnings

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

warnings.filterwarnings("ignore", message="Ignoring wrong pointing object")


# Initialize embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Path setup
finance_docs_path = r'DS-RPC-01/data/finance'
db_path = r'vector_dbs/finance'

# Check if DB already exists
if os.path.exists(db_path) and len(os.listdir(db_path)) > 0:
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    print("Loaded existing Chroma DB.")
else:
    # Load markdown files
    loader = DirectoryLoader(finance_docs_path, glob="**/*.md", loader_cls=TextLoader, recursive=True)
    docs = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(docs)

    # Create & persist Chroma DB
    db = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=db_path)
    db.persist()  # Only called after from_documents
    print("Created and saved new Chroma DB.")

# Create retriever
finance_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
print("Retriever is ready.")