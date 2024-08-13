import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from bot.config.logging_config import app_logger
from bot.setting.config import config

# Bot commands
difficulty_button1 = KeyboardButton("easy")
difficulty_button2 = KeyboardButton("medium")
difficulty_button3 = KeyboardButton("hard")
difficulty_button4 = KeyboardButton("none")
difficulty_keyboard = ReplyKeyboardMarkup(
    [[difficulty_button1, difficulty_button2, difficulty_button3, difficulty_button4]],
    resize_keyboard=True, one_time_keyboard=True)

answers_button1 = KeyboardButton("1")
answers_button2 = KeyboardButton("2")
answers_button3 = KeyboardButton("3")
answers_button4 = KeyboardButton("4")
answers_keyboard = ReplyKeyboardMarkup([[answers_button1, answers_button2], [answers_button3, answers_button4]],
                                       resize_keyboard=True, one_time_keyboard=True)

DIFFICULTY, ANSWERS, TOPIC, USER_ANSWER = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, public_ip: str) -> None:
    message = f"Hello! This is your bot.\nPublic IP: {public_ip}"
    app_logger.info(message)
    await update.message.reply_text(message)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    app_logger.info(f"User {update.effective_user.username} ({update.effective_user.id}) triggered help command.")

    help_message = (
        "Here are the commands you can use:\n"
        "/start - Start the bot and display a welcome message.\n"
        "/help - Display this help message.\n"
        "/connect - Connect to the server and retrieve a message.\n"
        "/question - Start the process of getting a question.\n"
        "/cancel - Cancel the current operation.\n"
        "\nTo get a question you need to use /question\n"
        "You will be asked to enter the required information:\n"
        "1. First, enter a difficulty level (easy, medium, hard, none).\n"
        "2. Then, enter the number of answers (1-4).\n"
        "3. Finally, enter the topic for the question."
    )

    await update.message.reply_text(help_message)
    app_logger.info("Help message sent successfully")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        user_id = update.effective_user.id
        username = update.effective_user.username
        app_logger.info(f"User {username} ({user_id}) triggered cancel command.")

        # Determine what operation was canceled
        if 'operation' in context.user_data:
            operation = context.user_data.pop('operation')
            message = f"The operation '{operation}' has been canceled."
            app_logger.info(f"User {username} ({user_id}) canceled the operation: {operation}")
        else:
            message = "There was no active operation to cancel."
            app_logger.info(f"User {username} ({user_id}) attempted to cancel, but no operation was active.")

        await update.message.reply_text(message)
    except Exception as e:
        app_logger.error(f"Error during cancellation for user {username} ({user_id}): {e}")
        await update.message.reply_text("An error occurred while attempting to cancel the operation. Please try again later.")

    return ConversationHandler.END


async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        app_logger.info(f"User {update.effective_user.username} ({update.effective_user.id}) triggered connect command.")
        response = requests.get(f"{config.SERVER_URL}/")
        response.raise_for_status()
        data = response.json()
        app_logger.info("Connection successful, sending response message")
        await update.message.reply_text(data["message"])
    except requests.RequestException as e:
        app_logger.error(f"Error fetching data for user {update.effective_user.username} ({update.effective_user.id}): {e}")
        await update.message.reply_text(f"Error fetching data: {e}")