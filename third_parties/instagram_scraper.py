import os
import requests
from dotenv import load_dotenv
load_dotenv()


token = os.getenv("APIFY_TOKEN")
if not token:
    raise ValueError("APIFY_TOKEN não encontrada no .env!")

def scrape_instagram_profile(username: str) -> dict:
    """Função para buscar dados de um perfil do Instagram usando o Apify
    Args:
        username (str): Nome de usuário do Instagram
    Returns: 
        dict: Dicionário com os dados do perfil (full_name, url, bio, followers, picture)
    """
    # token = os.getenv("APIFY_TOKEN")
    # if not token:
    #     raise ValueError("APIFY_TOKEN não encontrada no .env!")

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

    json =  response.json()

    full_name = json[0].get("fullName")
    url = json[0].get("url")
    bio = json[0].get("biography")
    followers = json[0].get("followersCount")
    picture = json[0].get("profilePictureUrl")

    return {
        "full_name": full_name,
        "url": url,
        "bio": bio,
        "followers": followers,
        "picture": picture
    }