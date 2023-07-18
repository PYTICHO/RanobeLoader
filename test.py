import requests
from bs4 import BeautifulSoup

user_agent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

url = r"https://ranobelib.me/incha-no-boku-ni-sefure-ga-iru-koto-wo-kurasu-no-kimi-tachi-ha-mada-shiranai/v1/c1?ui=5279067"
login_url = r"https://lib.social/login"
profile_url = r"https://ranobelib.me/user/5279067"

session = requests.Session()
session.headers.update({'User-Agent': user_agent})

# respons = session.get("https://lib.social/login").text
# #XSRF, CSRF токены чтобы сайт не блокировал запросы
# XSRF = session.cookies['XSRF-TOKEN']
# CSRF = respons.split('<meta name="_token" content="')[1].split('">')[0]

# headers = {
#     'X-CSRF-TOKEN': CSRF,
#     'X-XSRF-TOKEN': XSRF
#     }


response1 = session.get(login_url)

soup = BeautifulSoup(response1.text, "html.parser")
token = soup.find('input', {'name': '_token'}).get('value')

data = {
    "_token": token,
    "from": "https://ranobelib.me/?section=home-updates",
    "email": "kasaev_2006@inbox.ru",
    "password": "Qwertyqwerty2006",
    "remember": "on"
}

response2 = session.post(login_url, data=data)


response3 = session.get(url)

print(response3.text)