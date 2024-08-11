from telegram import Update
from telegram.ext import ContextTypes
import requests
from bot.setting.config import config


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    response = requests.get( f"{config.SERVER_URL}/quote/{user_id}").json()
    quote = response["quote"]
    author = response["author"]

    reply = f'"{quote}" - {author}'
    await update.message.reply_text(reply)