import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DEBUG = True

TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")

