from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import (
    AgentExecutor, 
    create_react_agent
)
from tools.instagram_scraper import scrape_instagram_profile
from tools.X_scraper import scrape_x_profile
from dotenv import load_dotenv
import os
import json


def lookup_agent(name: str):
    """Enhanced version with comprehensive error handling and logging."""
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file!")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        api_key=api_key
    )

    tools_for_agent = [
        Tool(
            name="scrape_instagram_profile",
            func=lambda username: json.dumps(scrape_instagram_profile(username)),
            description="Function to fetch Instagram profile data using Apify. Returns a dictionary with profile data (full_name, url, bio, followers, picture)."
        ),
        Tool(
            name="scrape_x_profile",
            func=lambda username: json.dumps(scrape_x_profile(username)),
            description="Function to fetch X (Twitter) profile data using Apify. Returns a dictionary with profile data (name, username, bio, followers, following, image)."
        )
    ]

    lookup_agent_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are an agent that looks up profiles on Instagram and Twitter using tools.\n"
        "You have access to the following tools:\n{tools}\n\n"
        "The tool names are: {tool_names}\n\n"
        "When given a name or username, you must use these tools to retrieve profile data.\n"
        "If both profiles are found, prefer Instagram data.\n"
        "Use the tools wisely and document your reasoning step by step.\n\n"
        "Format your response **exactly** as:\n"
        "Thought: [Your reasoning here]\n"
        "Action: [Tool name exactly as provided in tool_names]\n"
        "Action Input: [Tool input here, e.g., username]"
    ),
    HumanMessagePromptTemplate.from_template("{input}\n\n{agent_scratchpad}")
])

    lookup_agent = create_react_agent(llm, tools_for_agent, lookup_agent_prompt)

    lookup_executor = AgentExecutor(
        agent=lookup_agent, 
        tools=tools_for_agent, 
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3
    )

    try:
        result = lookup_executor.invoke({"input": f"{name}"})
        
        return {
            "status": "success",
            "output": result.get("output", ""),
            "username": name
        }

        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "username": name
        }