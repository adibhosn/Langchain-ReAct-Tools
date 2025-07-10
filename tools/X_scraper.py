from langchain_core.tools import Tool
import os
import requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("APIFY_TOKEN")
if not token:
    raise ValueError("APIFY_TOKEN não encontrada no .env!")

def scrape_x_profile(username: str) -> dict:
    """Function to fetch Instagram profile data using Apify
    Args:
        username (str): Instagram username
    Returns: 
        dict: Dictionary with profile data (full_name, url, bio, followers, picture)
    """
    ACTOR_URL = f"https://api.apify.com/v2/acts/epctex~twitter-profile-scraper/run-sync-get-dataset-items?token={token}"

    payload = {
        "usernames": [username],
        "maxProfiles": 1
    }

    response = requests.post(ACTOR_URL, json=payload)
    response.raise_for_status()
    json_data = response.json()

    if not json_data:
        return {}

    user = json_data[0]
    return {
        "name": user.get("name"),
        "username": user.get("username"),
        "bio": user.get("description"),
        "followers": user.get("followersCount"),
        "following": user.get("friendsCount"),
        "profilepicture": user.get("profileImageUrl"),
    }
