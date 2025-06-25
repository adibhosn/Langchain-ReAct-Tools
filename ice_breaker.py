from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

question = "What is the capital of France?"

if __name__ == '__main__':
    load_dotenv()  # Carrega as variáveis do .env

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada no .env!")

    summary_template = (
        "You are a helpful assistant.\n"
        "Answer the following question: {question}"
    )

    prompt_template = PromptTemplate(
        input_variables=["question"],
        template=summary_template
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        api_key=api_key
    )

    chain = prompt_template | llm

    response = chain.invoke({"question": question})

    print(response.content)