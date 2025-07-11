from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from agents.lookup_agent import lookup_agent
import os

if __name__ == '__main__':
    load_dotenv()  # Carrega as variáveis do .env
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada no .env!")
    
    username = "cristiano"
    profile_data = lookup_agent(username)
    if profile_data["status"] == "success":
        extracted_data = profile_data["output"]

        # Transformar para string legível
        formatted_profile_data = (
            f"Name: {extracted_data['full_name']}\n"
            f"Bio: {extracted_data['bio']}\n"
            f"Followers: {extracted_data['followers']}\n"
            f"Profile: {extracted_data['url']}"
        )
    else:
        raise Exception(f"Lookup failed: {profile_data['error']}")

    system_prompt = SystemMessagePromptTemplate.from_template(
        """
    You are an assistant specialized in generating clear, concise, and informative summaries of social media profiles.
    """
    )
    
    user_msg = HumanMessagePromptTemplate.from_template("""Based on the following data extracted from the user, write a short paragraph describing the person:
    
    {profile_data}
    
    Guidelines:
    - Introduce the person by name and highlight relevant details from the biography.
    - Provide context about the follower count (e.g., "has a substantial following of over 50,000 people").
    - Do not mention that the data came from an API or scraping.
    - Write in third person, using a neutral and professional tone.
    - Keep the summary concise, ideally under 100 words.
    """)

    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, user_msg])
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        api_key=api_key
    )

    chain = chat_prompt | llm

    response = chain.invoke({"profile_data": formatted_profile_data})

    print(response.content)