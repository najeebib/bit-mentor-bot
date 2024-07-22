from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
from handlers.some_handler import *
import requests
load_dotenv()
SERVER_ADDRESS = os.getenv('SERVER_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the /start command with the start function
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()