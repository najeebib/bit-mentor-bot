import os
import requests
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
import logging.config
from bot.config.logging_config import logging_config
from bot.handlers.basic_fns import start, connect

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip = response.json()['ip']
        logger.info(f"Fetched public IP: {ip}")
        return ip
    except Exception as e:
        logger.error("Error fetching public IP", exc_info=True)
        raise

def main():
    logger.info("Starting bot application")
    # Fetch the public IP address
    public_ip = get_public_ip()

    # Create the Application and pass it your bot's token
    try:
        BOT_TOKEN = os.getenv('BOT_TOKEN')
        if BOT_TOKEN:
            application = Application.builder().token(BOT_TOKEN).build()
            # Register the /start command with the start function
            start_handler = CommandHandler('start', lambda update, context: start(update, context, public_ip))
            connect_handler = CommandHandler('connect', lambda update, context: connect(update, context))

            application.add_handler(start_handler)
            application.add_handler(connect_handler)

            logger.info("Bot handlers added and polling started")
            # Start the Bot
            application.run_polling()
        else:
            raise Exception("BOT_TOKEN not loaded correctly as env var")
    except Exception as e:
        logger.error("Error in loading BOT_TOKEN", exc_info=True)
        raise

if __name__ == '__main__':
    main()
