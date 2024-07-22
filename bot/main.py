import os
import requests
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from bot.handlers.some_handler import start, connect

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
SERVER_URL = os.getenv('SERVER_URL')

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    response.raise_for_status()
    return response.json()['ip']

def main():
    # Fetch the public IP address
    public_ip = get_public_ip()

    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the /start command with the start function
    start_handler = CommandHandler('start', lambda update, context: start(update, context, public_ip))
    connect_handler = CommandHandler('connect', lambda update, context: connect(update, context))

    application.add_handler(start_handler)
    application.add_handler(connect_handler)

    # Start the Bot
    application.run_polling()

     # Set up webhook
    webhook_url = f"{SERVER_URL}/{BOT_TOKEN}"
    application.bot.set_webhook(webhook_url)

    # Start the webhook
    application.run_webhook(listen="0.0.0.0", port=int(os.environ.get('PORT', 8443)), url_path=BOT_TOKEN)

if __name__ == '__main__':
    main()
