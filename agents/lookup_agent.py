from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import (
    AgentExecutor, 
    create_react_agent
)
from tools.instagram_scraper import scrape_instagram_profile
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel, Field
from typing import Optional



class ProfileData(BaseModel):
    full_name: str = Field(..., description="Full name of the user")
    url: str = Field(..., description="Profile URL")
    bio: str = Field(..., description="Biography of the user")
    followers: int = Field(..., description="Number of followers")
    picture: Optional[str] = None



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
        )]


    lookup_agent_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are an agent that retrieves Instagram profile data using tools.\n"
            "You have access to the following tools:\n{tools}\n\n"
            "The tool names are: {tool_names}\n\n"
            "You must output the final answer as a valid JSON object with the following keys:\n"
            "full_name (string), url (string), bio (string), followers (integer), picture (string or null).\n"
            "No explanations, no extra commentary — only the JSON.\n\n"
            "Use this format:\n"
            "Thought: [your reasoning]\n"
            "Action: [tool name]\n"
            "Action Input: [username]\n"
            "Observation: [result]\n"
            "Final Answer: [the JSON described above]"
            "You must always end with 'Final Answer' containing the valid JSON object as specified."

        ),
        HumanMessagePromptTemplate.from_template("{input}\n\n{agent_scratchpad}")
    ])

    lookup_agent = create_react_agent(
        llm,
        tools_for_agent,
        lookup_agent_prompt.partial(
            tools="\n".join(f"{tool.name}: {tool.description}" for tool in tools_for_agent),
            tool_names=", ".join(tool.name for tool in tools_for_agent)
        )
    )

    lookup_executor = AgentExecutor(
        agent=lookup_agent, 
        tools=tools_for_agent, 
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3
    )

    try:
        result = lookup_executor.invoke({"input": f"{name}"})

        # Validação e parsing do output
        if "output" in result:
            json_output = json.loads(result["output"])  # Converte JSON string para dict
            structured_output = ProfileData.parse_obj(json_output)  # Valida com Pydantic
            return {
                "status": "success",
                "output": structured_output.dict(),
                "username": name
            }
        else:
            return {
                "status": "error",
                "error": "No output found",
                "username": name
            }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "username": name
        }