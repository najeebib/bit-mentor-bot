import requests
import os
from telegram import Update
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from bot.config.logging_config import logging_config
from loguru import logger
from bot.setting.config import config


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, public_ip: str) -> None:
    message = f"Hello! This is your bot.\nPublic IP: {public_ip}"
    logger.info(f"Sending start message: {message}")
    await update.message.reply_text(message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "To get a question you need to use /question\n"
        "You will be asked to enter the required information\n"
        "First you need to enter a difficulty\n"
        "Then enter the number of answers\n"
        "Then enter the topic"
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation canceled.")
    return ConversationHandler.END


async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(f"{config.SERVER_URL}/")
        response.raise_for_status()
        data = response.json()
        logger.info("Connection successful, sending response message")
        await update.message.reply_text(data["message"])
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        await update.message.reply_text(f"Error fetching data: {e}")
