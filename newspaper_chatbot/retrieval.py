

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


# Define Prompt Template
chat_prompt = """You are an AI chatbot that is friendly and helpful.
    There are some rules you must follow:
    1. Only respond to non-vernacular questions.
    2. Always give short and concise answers.
    3. If there is more than one point then answer in bullet points.

    User Question: {question}
    Context: {context}
    """

chat_template = ChatPromptTemplate.from_template(chat_prompt)


# Define the chatbot pipeline using ONLY chatbot
chatbot = (
    {"question":RunnablePassthrough(),"context":RunnablePassthrough()}
    |chat_template
    |llm
    |StrOutputParser()
)


# Function to get top documents from retriever
def get_context(user_query):
    top_docs = retriever.invoke(user_query)
    return [doc.page_content for doc in top_docs]


# Chatbot loop
def run_chatbot():
    print("\033c", end="")  # Clear terminal
    print("++==================================================++")
    print("Bot: Hello, how can I help you? Type 'exit' to quit.")

    while True:
        user_input = input("\nUser: ")
        if user_input.strip().lower() == "exit":
            break
    
        context_docs = get_context(user_input)
        response = chatbot.invoke({"question": user_input, "context": context_docs})
        print(f"Bot: {response}")

        
# ✅ Run chatbot interactively
run_chatbot()
