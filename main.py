import pprint
import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from os.path import join, dirname

def shorten_link(longLink, TOKEN):
    headers = {'Authorization': f"Bearer {TOKEN}"}
    response = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=headers, json={"long_url": longLink})
    response.raise_for_status()
    response_json = response.json()
    return response_json['link']


def count_clicks(link, token):
    url_obj = urlparse(link)
    headers = {'Authorization': f"Bearer {token}"}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{url_obj.netloc}{url_obj.path}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    return response_json['total_clicks']


def is_bitlink(url, token):
    url_obj = urlparse(url)
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{url_obj.netloc}{url_obj.path}", headers=headers)
    return response.ok


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    try:
        token = os.environ["BITLY_TOKEN"]
    except KeyError:
        print("Вы не заполнили токен")
        exit()

    print("Введите ссылку:")
    user_input = input()

    bitlnk = is_bitlink(user_input, token)
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




