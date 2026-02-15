import requests
from bs4 import BeautifulSoup
import re
import time

STEAM_API_KEY = "ECEE2172241E029235BA9C59A6A7A50F"



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


def get_faceit_data(user_input):
    headers = {"User-Agent": "Mozilla/5.0"}
    user_input = user_input.strip()

    if "steamcommunity.com" in user_input:

        if "/profiles/" in user_input:
            steam_id = user_input.split("/profiles/")[1].split("/")[0]

        elif "/id/" in user_input:
            vanity = user_input.split("/id/")[1].split("/")[0]
            steam_id = resolve_vanity_url(vanity)

            if not steam_id:
                return {"error": "Не удалось получить SteamID64"}

        else:
            return {"error": "Неверная Steam ссылка"}

    else:
        if user_input.isdigit():
            steam_id = user_input
        else:
            steam_id = resolve_vanity_url(user_input)
            if not steam_id:
                return {"error": "Не удалось определить SteamID64"}

    url = f"https://faceitfinder.com/profile/{steam_id}"
    response = requests.get(url, headers=headers, allow_redirects=True)

    if response.status_code != 200:
        return {"error": f"Ошибка загрузки ({response.status_code})"}

    if "No Faceit account found" in response.text:
        return {"error": "Faceit аккаунт не найден"}

    soup = BeautifulSoup(response.text, "html.parser")

    nickname_tag = soup.find("span", class_="account-faceit-title-username")
    nickname = nickname_tag.text.strip() if nickname_tag else "Не найден"

    level = "0"
    level_img = soup.find("img", src=re.compile(r"skill_level_\d+_lg\.png"))
    if level_img:
        match = re.search(r"skill_level_(\d+)_lg\.png", level_img["src"])
        if match:
            level = match.group(1)

    stats_blocks = soup.find_all("div", class_="account-faceit-stats-single")

    kd = elo = matches = hs = "Не найден"

    for block in stats_blocks:
        text = block.text.strip()
        strong = block.find("strong")
        if not strong:
            continue

        value = strong.text.strip()

        if "K/D" in text:
            kd = value
        elif "ELO" in text:
            elo = value
        elif "Matches" in text:
            matches = value
        elif "HS" in text:
            hs = value

    return {
        "nickname": nickname,
        "level": int(level),
        "elo": elo,
        "kd": kd,
        "matches": matches,
        "hs": hs
    }

def get_player_stats(user_input: str) -> str:
    data = get_faceit_data(user_input)

    if "error" in data:
        return f"Ошибка: {data['error']}"

    result_text = f"""
Ник: {data['nickname']}
Level: {data['level']}
ELO: {data['elo']}
K/D: {data['kd']}
HS: {data['hs']}
Matches: {data['matches']}
    """

    return result_text.strip()


if __name__ == "__main__":
    steam_input = input("Вставь SteamID: ")
    print(get_player_stats(steam_input))