import requests
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from bot.handlers.basic_fns import *
from bot.handlers.question_handlers import *
from bot.handlers.user_handlers import *
from bot.setting.config import *

DIFFICULTY, ANSWERS, TOPIC, USER_ANSWER = range(4)

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    response.raise_for_status()
    return response.json()['ip']


# Main function
def main():
    # Fetch the public IP address
    public_ip = get_public_ip()

    # Create the Application and pass it your bot's token
    try:
        BOT_TOKEN = config.BOT_TOKEN
        if BOT_TOKEN:
            application = Application.builder().token(BOT_TOKEN).build()
            # Register the /start command with the start function
            start_handler = CommandHandler('start', lambda update, context: start(update, context, public_ip))
            connect_handler = CommandHandler('connect', connect)
            help_handler = CommandHandler('help', help)

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
            application.add_handler(help_handler)

            # Start the Bot
            application.run_polling()
        else:
            raise Exception("BOT_TOKEN not loaded correctly as env var")
    except Exception as e:
        print("error in loading BOT_TOKEN", e)
        return e

if __name__ == '__main__':
    main()