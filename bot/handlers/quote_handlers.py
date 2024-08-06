from telegram import Update
from telegram.ext import ContextTypes
import requests
from bot.setting.config import config


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get( f"{config.SERVER_URL}/quote").json()
    quote = response[0]["quote"]

    await update.message.reply_text(quote)