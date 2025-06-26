from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()  # Carrega as variáveis do .env

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada no .env!")

    system_msg = SystemMessagePromptTemplate.from_template("You will answer all the questions wrong, making up a convincing reason")
    user_msg = HumanMessagePromptTemplate.from_template("What is the capital of France?")

    chat_prompt = ChatPromptTemplate.from_messages([system_msg, user_msg])
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        api_key=api_key
    )

    chain = chat_prompt | llm

    response = chain.invoke({})

    print(response)