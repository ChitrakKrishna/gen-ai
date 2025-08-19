from admin import department  # ✅ Assumes department is defined in admin.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def get_retrievers(department: str):
    """
    Import department-specific retriever (if available)
    + always import general retriever.
    Return both in a tuple: (department_retriever, general_retriever)
    """
    department = department.strip().lower()

    from rag.general import general_retriever

    mapping = {
        'engineering': ('engineer', 'engineer_retriever'),
        'finance': ('finance', 'finance_retriever'),
        'marketing': ('marketing', 'marketing_retriever'),
        'hr': ('hr', 'hr_retriever'),
        'sales': ('marketing', 'marketing_retriever'),
        'business': (None, None),
        'quality assurance': ('engineer', 'engineer_retriever'),
        'operations': (None, None),
        'technology': ('engineer', 'engineer_retriever'),
        'compliance': ('finance', 'finance_retriever'),
        'data': ('engineer', 'engineer_retriever'),
        'risk': ('finance', 'finance_retriever'),
        'product': ('marketing', 'marketing_retriever'),
        'design': ('marketing', 'marketing_retriever')
    }

    module_name, _ = mapping.get(department, (None, None))

    dept_retriever = None

    if module_name == 'hr':
        from rag.hr import hr_retriever
        dept_retriever = hr_retriever
    elif module_name == 'marketing':
        from rag.marketing import marketing_retriever
        dept_retriever = marketing_retriever
    elif module_name == 'finance':
        from rag.finance import finance_retriever
        dept_retriever = finance_retriever
    elif module_name == 'engineer':
        from rag.engineer import engineer_retriever
        dept_retriever = engineer_retriever

    return dept_retriever, general_retriever


llm = ChatGroq(
    model=os.getenv("ModelName"),
    temperature=0.9,
    api_key=os.getenv("ChatGroqAPIKey")
)

with open("DS-RPC-01/metadata.txt", "r") as f:
    instructions = f.read()

chat_prompt = """You are an AI chatbot that is friendly and helpful.
You only answer questions related to the context.
Rules:
1. Only answer questions that are not vernacular.
2. Always give short and concise answers.
3. Always answer in short points.

This is the user's question: {question}
And this is the Context: {context}
"""

full_prompt = instructions + "\n\n" + chat_prompt

chatTemp = ChatPromptTemplate.from_template(full_prompt)

chatbot = (
    {"question": RunnablePassthrough(), "context": RunnablePassthrough()}
    | chatTemp
    | llm
    | StrOutputParser()
)




def get_response(department, user_input):
    dept_retriever, general_retriever = get_retrievers(department)

    dept_docs = []
    if dept_retriever is not None:
        dept_docs = dept_retriever.invoke(user_input)

    general_docs = general_retriever.invoke(user_input)
    documents = [doc.page_content for doc in dept_docs + general_docs]

    response = chatbot.invoke({"question": user_input, "context": documents})
    return response




if __name__ == "__main__":
    print("\033c", end="")
    print("++==================================================++")
    print("Bot: Hello, how can I help?")

    while True:
        user_input = input("\nUser: ")
        if user_input.strip().lower() == "exit":
            break

        dept_retriever, general_retriever = get_retrievers(department)

        dept_docs = []
        if dept_retriever is not None:
            dept_docs = dept_retriever.invoke(user_input)

        general_docs = general_retriever.invoke(user_input)
        documents = [doc.page_content for doc in dept_docs + general_docs]

        response = chatbot.invoke({"question": user_input, "context": documents})
        print(f"Bot: {response}")
