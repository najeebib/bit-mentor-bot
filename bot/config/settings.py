import os
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
