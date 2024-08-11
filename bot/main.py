import requests
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from bot.handlers.basic_fns import *
from bot.handlers.question_handlers import *
from bot.handlers.user_handlers import *
from bot.setting.config import *
from bot.config.logging_config import logger





def get_public_ip():
    try:
        logger.info("Fetching public IP address")
        response = requests.get('https://api.ipify.org?format=json')
        logger.info(f"Request made to IPify API, status code: {response.status_code}")
        response.raise_for_status()
        ip = response.json()['ip']
        logger.info(f"Fetched public IP: {ip}")
        return ip
    except Exception as e:
        logger.error("Error fetching public IP", exc_info=True)
        raise

def main():
    logger.info("Starting bot application")
    try:
        public_ip = get_public_ip()
        logger.info(f"Fetched public IP: {public_ip}")

        BOT_TOKEN = config.BOT_TOKEN
        logger.info(f"BOT_TOKEN loaded: {'Yes' if BOT_TOKEN else 'No'}")
        if BOT_TOKEN:
            logger.info("Creating application with bot token")
            application = Application.builder().token(BOT_TOKEN).build()

            # Adding command handlers, including the help command
            start_handler = CommandHandler('start', lambda update, context: start(update, context, public_ip))
            connect_handler = CommandHandler('connect', connect)
            help_handler = CommandHandler('help', help_command)  # Added help_handler
            conv_handler = ConversationHandler(
                entry_points=[CommandHandler('question', question_command)],
                states={
                    DIFFICULTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, difficulty_response)],
                    ANSWERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, answers_response)],
                    TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic_response)],
                    USER_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_answer_response)],
                },
                fallbacks=[CommandHandler('cancel', cancel)],
            )

            application.add_handler(conv_handler)
            application.add_handler(start_handler)
            application.add_handler(connect_handler)
            application.add_handler(help_handler)  # Registered help_handler

            logger.info("Bot handlers added and polling started")
            application.run_polling()
        else:
            logger.error("BOT_TOKEN not loaded correctly as env var")
            raise Exception("BOT_TOKEN not loaded correctly as env var")
    except Exception as e:
        logger.error("Error in main function", exc_info=True)
        raise

if __name__ == '__main__':
    main()
