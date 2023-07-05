import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from os.path import join, dirname
import argparse


def shorten_link(long_link, token):
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=headers, json={"long_url": long_link})
    response.raise_for_status()
    response_data = response.json()
    return response_data['link']


def count_clicks(link, token):
    url_obj = urlparse(link)
    headers = {'Authorization': f"Bearer {token}"}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{url_obj.netloc}{url_obj.path}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data['total_clicks']


def is_bitlink(url, token):
    url_obj = urlparse(url)
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{url_obj.netloc}{url_obj.path}", headers=headers)
    return response.ok


def main():
    parser = argparse.ArgumentParser(
        description='Вводите ссылку получаете количество кликов по ней или ее короткую версию'
    )
    parser.add_argument('-u', '--url', help='Ваша ссылка')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    try:
        token = os.environ["BITLY_TOKEN"]
    except KeyError:
        print("Вы не заполнили токен")
        return

    if not args.url:
        print("Введите ссылку:")
        user_input = input()
    else:
        user_input = args.url

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


if __name__ == '__main__':
    main()

