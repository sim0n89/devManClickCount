import pprint
import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from os.path import join, dirname

def shorten_link(longLink, TOKEN):
    headers = {'Authorization': f"Bearer {TOKEN}"}
    r = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=headers, json={"long_url": longLink})
    r.raise_for_status()
    json = r.json()
    return json['link']


def count_clicks(link, token):
    parse = urlparse(link)
    headers = {'Authorization': f"Bearer {token}"}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{parse.netloc}{parse.path}/clicks/summary"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    json = r.json()
    return json['total_clicks']


def is_bitlink(url, token):
    parse = urlparse(url)
    headers = {'Authorization': f"Bearer {token}"}
    r = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{parse.netloc}{parse.path}", headers=headers)
    r.raise_for_status()
    return True


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    token = os.environ.get("BITLY_TOKEN")
    print("Введите ссылку:")
    user_input = input()

    try:
        bitlnk = is_bitlink(user_input, token)
    except requests.exceptions.HTTPError as e:
        bitlnk = False

    if bitlnk:
        try:
            clicks = count_clicks(user_input, token)
            print("Общее число кликов:", clicks)
        except requests.exceptions.HTTPError as e:
            print(e)
    else:
        try:
            bitlink = shorten_link(user_input, token)
            print(bitlink)
        except requests.exceptions.HTTPError:
            print("Вы ввели неверную ссылку")




