#.\venv\Scripts\activate

# Import necessary modules from langchain for document loading, text splitting, embeddings, vector storage and QA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq  # type: ignore
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from rag import retriever
import os

from dotenv import load_dotenv
load_dotenv()

apigroq = os.getenv('ChatGroqAPIKey')
model = os.getenv('ModelName')
api = os.getenv('APIKey')


llm = ChatGroq(
    api_key=apigroq,        # type: ignore
    model="llama-3.3-70b-versatile",
    temperature=0.4
)

from langchain.chains import LLMChain

prompt_template_name = PromptTemplate(
    input_variables =['topic'],
    template = "Generate the a title related to {topic} for my YouTube Channel. Just give title in output"
)
topic_name =LLMChain(llm=llm, prompt=prompt_template_name)


prompt_template_segments = PromptTemplate(
    input_variables =['name_suggestions'],
    template = "Give me around 10 segments for each {name_suggestions}. Don't provide the background."
)
segment = LLMChain(llm=llm, prompt=prompt_template_segments, output_key="segments")


prompt_template_script = PromptTemplate(
    input_variables =['segments','context'],
    template = "Based on the following segments: {segments}, write a detailed script that covers all important points."
)
script = LLMChain(llm=llm, prompt=prompt_template_script, output_key="script")

from langchain.chains import SimpleSequentialChain
chain = SimpleSequentialChain(chains = [topic_name, segment, script],verbose=True)

import json

# Function to generate YouTube script
def chatbot(query: str):
    print("\nGenerating YouTube script...\n")
    full_script = chain.invoke(query)


    # Try extracting output, fallback to full JSON string
    output_text = (
        full_script.get("text") or
        full_script.get("output") or
        json.dumps(full_script)
        if isinstance(full_script, dict)
        else str(full_script)
    )

    # Save to file
    filename = f"{query}_youtube_script.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output_text) 
        

    print(f"\nScript saved to: {filename}")
    return output_text



# Chatbot loop
def run_chatbot():
    print("\033c", end="")  # Clear terminal
    print("++==================================================++")
    print("Bot: Hello! Type a YouTube topic to generate a script, or type 'exit' to quit.")

    while True:
        user_input = input("\nUser: ")
        if user_input.strip().lower() == "exit":
            print("Bot: Goodbye!")
            break

        response = chatbot(user_input)

# Run the script if this is the main file
if __name__ == "__main__":
    run_chatbot()


# ✅ Run chatbot interactively
run_chatbot()