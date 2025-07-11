from langchain_core.tools import Tool
import os
import requests
from dotenv import load_dotenv
load_dotenv()


token = os.getenv("APIFY_TOKEN")
if not token:
    raise ValueError("APIFY_TOKEN não encontrada no .env!")

def scrape_instagram_profile(username: str) -> dict:
    """Function to fetch Instagram profile data using Apify
    Args:
        username (str): Instagram username
    Returns: 
        dict: Dictionary with profile data (full_name, url, bio, followers, picture)
    """
    try:
        ACTOR_URL = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={token}"

        # Input da requisição
        payload = {
            "addParentData": False,
            "directUrls": [
                f"https://www.instagram.com/{username}/"
            ],
            "enhanceUserSearchWithFacebookPage": False,
            "isUserReelFeedURL": False,
            "isUserTaggedFeedURL": False,
            "resultsLimit": 1,
            "resultsType": "details",  # MUITO IMPORTANTE!
        }

        # Faz a requisição
        response = requests.post(ACTOR_URL, json=payload)
        response.raise_for_status()  # Levanta exceção para status HTTP de erro
        
        json_data = response.json()
        
        # Verifica se a resposta não está vazia
        if not json_data or len(json_data) == 0:
            return {
                "error": f"No data found for username: {username}",
                "full_name": None,
                "url": None,
                "bio": None,
                "followers": None,
                "picture": None
            }

        user_data = json_data[0]
        
        return {
            "full_name": user_data.get("fullName"),
            "url": user_data.get("url"),
            "bio": user_data.get("biography"),
            "followers": user_data.get("followersCount"),
            "picture": user_data.get("profilePictureUrl")
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {str(e)}",
            "full_name": None,
            "url": None,
            "bio": None,
            "followers": None,
            "picture": None
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "full_name": None,
            "url": None,
            "bio": None,
            "followers": None,
            "picture": None
        }