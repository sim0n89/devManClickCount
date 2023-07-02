import os
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
BITLY_TOKEN = os.environ.get("TOKEN")