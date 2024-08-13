from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from bot.handlers.basic_handlers import *
from bot.handlers.middleware import request_logging_middleware

from bot.handlers.youtube_handler import mark_video_watched_callback
from bot.handlers.quote_handlers import quote_command
from bot.setting.config import *

from bot.utils.public_ip import get_public_ip
from bot.handlerConversation.youtubeConversation import youtube_conversation
from bot.handlerConversation.question_conversation import question_conversation
from bot.handlerConversation.task_conversation import task_conversation


def main():
    app_logger.info("Starting bot application")
    public_ip = get_public_ip()
    try:
        BOT_TOKEN = config.BOT_TOKEN
        if BOT_TOKEN:
            application = Application.builder().token(BOT_TOKEN).build()


            # basic
            # Adding command handlers, including the help command
            start_handler = CommandHandler('start', request_logging_middleware(start, public_ip=public_ip))
            connect_handler = CommandHandler('connect', request_logging_middleware(connect))
            help_handler = CommandHandler('help', request_logging_middleware(help))

            quote_handler = CommandHandler('quote',  lambda update, context: quote_command(update, context))
            
            # youtube
            application.add_handler(youtube_conversation())
            application.add_handler(CallbackQueryHandler(mark_video_watched_callback))

            application.add_handler(question_conversation())
            application.add_handler(task_conversation())

            application.add_handler(start_handler)
            application.add_handler(connect_handler)
            application.add_handler(help_handler)
            application.add_handler(quote_handler)

            app_logger.info("Bot handlers added and polling starting")
            application.run_polling()
            app_logger.info("polling finished successfully")
        else:
            app_logger.error("BOT_TOKEN not loaded correctly as env var")
            raise Exception("BOT_TOKEN not loaded correctly as env var")
    except Exception as e:
        app_logger.error("Error in loading BOT_TOKEN", exc_info=True)
        raise e


if __name__ == '__main__':
    main()
