import pprint
import requests
from urllib.parse import urlparse
from config import TOKEN


def get_profile():
    headers = {'Authorization': f"Bearer {TOKEN}"}
    r = requests.get('https://api-ssl.bitly.com/v4/user', headers=headers)
    r.raise_for_status()
    pprint.pprint(r.json())


def shorten_link(longLink):
    headers = {'Authorization': f"Bearer {TOKEN}"}
    r = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=headers, json={"long_url": longLink})
    r.raise_for_status()
    json = r.json()
    return json['link']



def count_clicks(link):
    parse = urlparse(link)
    headers = {'Authorization': f"Bearer {TOKEN}"}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{parse.netloc}{parse.path}/clicks/summary"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    json = r.json()
    return json['total_clicks']


def is_bitlink(url):
    parse = urlparse(url)
    headers = {'Authorization': f"Bearer {TOKEN}"}
    r = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{parse.netloc}{parse.path}", headers=headers)
    r.raise_for_status()
    return True


if __name__ == '__main__':
    print("Введите ссылку:")
    user_input = input()

    try:
        bitlnk = is_bitlink(user_input)
    except requests.exceptions.HTTPError as e:
        bitlnk = False

    if bitlnk:
        try:
            clicks = count_clicks(user_input)
            print("Общее число кликов:", clicks)
        except requests.exceptions.HTTPError as e:
            print(e)
    else:
        try:
            bitlink = shorten_link(user_input)
            print(bitlink)
        except requests.exceptions.HTTPError:
            print("Вы ввели неверную ссылку")



