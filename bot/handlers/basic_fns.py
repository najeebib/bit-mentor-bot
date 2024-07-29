import requests
from telegram import Update
from telegram.ext import ContextTypes
from bot.setting.config import config


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, public_ip: str) -> None:
    message = f"Hello! This is your bot.\nPublic IP: {public_ip}"
    await update.message.reply_text(message)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "To get a question you need to use /question\nYou will be asked to enter the required information\nFirst you need to enter a difficulty\nThen enter the number of answers\nThen enter the topic")


async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    difficulty = "easy"
    topic = "python"
    response = requests.post(f"{config.SERVER_URL}/generate-question",
                             json={"difficulty": difficulty, "topic": topic}).json()

    await update.message.reply_text(response["question"])


async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(f"{config.SERVER_URL}/")
        response.raise_for_status()
        data = response.json()
        await update.message.reply_text(data["message"])
    except requests.RequestException as e:
        await update.message.reply_text(f"Error fetching data: {e}")
