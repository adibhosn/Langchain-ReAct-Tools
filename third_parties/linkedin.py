import os
import requests
from dotenv import load_dotenv
load_dotenv()




    
token = os.getenv("APIFY_TOKEN")
if not token:
    raise ValueError("APIFY_TOKEN não encontrada no .env!")

ACTOR_URL = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={token}"

# Input da requisição
payload = {
    "addParentData": False,
    "directUrls": [
        f"https://www.instagram.com/neymarjr/"
    ],
    "enhanceUserSearchWithFacebookPage": False,
    "isUserReelFeedURL": False,
    "isUserTaggedFeedURL": False,
    "onlyPostsNewerThan": "2025-06-24",
    "resultsLimit": 1,
    "resultsType": "details",  # MUITO IMPORTANTE!
    "searchLimit": 1,
    "searchType": "hashtag"
}

# Faz a requisição
response = requests.post(ACTOR_URL, json=payload)

# Trata a resposta
if response.status_code == 200:
    result = response.json()
    if result:
        perfil = result[0]  # Assume o primeiro item
        foto = perfil.get("profilePicUrl")
        bio = perfil.get("biography")

        print("📸 Foto de perfil:")
        print(foto)

        print("\n📝 Bio:")
        print(bio)
    else:
        print("Nenhum dado retornado.")
else:
    print(f"❌ Erro {response.status_code}: {response.text}")