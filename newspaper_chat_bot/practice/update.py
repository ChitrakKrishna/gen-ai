import os
import hashlib
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Step 1: Set up embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

# Step 2: Load existing FAISS index and collect existing hashes
index_path = "faiss_index"
existing_hashes = set()

if os.path.exists(index_path):
    vector_index = FAISS.load_local(index_path, embeddings)
    for doc in vector_index.docstore._dict.values():
        hash_val = hashlib.md5(doc.page_content.encode('utf-8')).hexdigest()
        existing_hashes.add(hash_val)
else:
    vector_index = None

# Step 3: Load new documents from URLs
urlLoader = UnstructuredURLLoader(urls=[
    "https://www.moneycontrol.com/news/business/banks/hdfc-bank-re-appoints-sanmoy-chakrabarti-as-chief-risk-officer-11259771.html",
    "https://www.moneycontrol.com/news/business/markets/market-corrects-post-rbi-ups-inflation-forecast-icrr-bet-on-these-top-10-rate-sensitive-stocks-ideas-11142611.html"
])
docs = urlLoader.load()

# Step 4: Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)

# Step 5: Filter out duplicate chunks
new_chunks = []
for chunk in chunks:
    hash_val = hashlib.md5(chunk.page_content.encode('utf-8')).hexdigest()
    if hash_val not in existing_hashes:
        new_chunks.append(chunk)
        existing_hashes.add(hash_val)

# Step 6: Add unique new chunks to the FAISS index
if new_chunks:
    if vector_index is None:
        vector_index = FAISS.from_documents(new_chunks, embeddings)
    else:
        vector_index.add_documents(new_chunks)

    vector_index.save_local(index_path)
    print(f"✅ Added {len(new_chunks)} new chunks to FAISS index.")
else:
    print("⚠️ No new unique content found. Index unchanged.")
