# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import LLMs
import langchain
from langchain_huggingface import HuggingFaceEndpoint
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

from langchain_community.embeddings import HuggingFaceEmbeddings
from rag import retriever

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA


llm = ChatGroq(
    model=os.getenv("ModelName"),        # type: ignore 
    temperature=0.9,
    api_key=os.getenv("ChatGroqAPIKey")  # type: ignore 
)


chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False   # Optional: returns source docs with the answer
)


langchain.debug = False

# Ask a question
query = "What is MPC? And what they are doing?"

response = chain({"query": query}, return_only_outputs=True)

# Print the response
print(response["result"])
