from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from third_parties.instagram_scraper import scrape_instagram_profile
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()  # Carrega as variáveis do .env

    username = "neymarjr"  
    profile_data = scrape_instagram_profile(username)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada no .env!")

    system_prompt = SystemMessagePromptTemplate.from_template(
        """
    You are an assistant specialized in generating clear, concise, and informative summaries of social media profiles.
    """
    )
    
    user_msg = HumanMessagePromptTemplate.from_template("""Based on the following data extracted from an Instagram profile, write a short paragraph describing the person:
    - Full name: {full_name}
    - Profile URL: {url}
    - Biography: {bio}
    - Follower count: {followers}
    - Profile picture URL: {picture}

    Guidelines:
    - Introduce the person by name and highlight relevant details from the biography.
    - Provide context about the follower count (e.g., "has a substantial following of over 50,000 people").
    - Do not mention that the data came from an API or scraping.
    - Write in third person, using a neutral and professional tone.
    - If any field is missing or empty, simply omit it from the summary without noting its absence.

    Output only the summary paragraph — no introductions, explanations, or additional formatting.
    """)

    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, user_msg])
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        api_key=api_key
    )

    chain = chat_prompt | llm

    response = chain.invoke(profile_data)

    print(response.content)