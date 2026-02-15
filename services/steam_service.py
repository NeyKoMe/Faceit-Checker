import requests
from config import STEAM_API_KEY

def resolve_vanity_url(vanity_url):
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {
        "key": STEAM_API_KEY,
        "vanityurl": vanity_url
    }

    response = requests.get(url, params=params)

    # 🔥 проверка статуса
    if response.status_code != 200:
        print("Ошибка Steam API:", response.status_code)
        return None

    # 🔥 проверка что ответ действительно JSON
    if not response.text.strip():
        print("Steam API вернул пустой ответ")
        return None

    try:
        data = response.json()
    except Exception:
        print("Steam API вернул не JSON:")
        print(response.text[:200])
        return None

    if data.get("response", {}).get("success") == 1:
        return data["response"]["steamid"]

    return None