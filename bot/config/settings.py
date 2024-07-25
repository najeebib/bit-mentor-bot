# bot/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SERVER_ADDRESS = os.getenv('SERVER_ADDRESS')
