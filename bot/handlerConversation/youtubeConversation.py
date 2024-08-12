from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

from bot.handlers.basic_handlers import cancel
from bot.handlers.middleware import request_logging_middleware
from bot.handlers.youtube_handler import start_youtube, get_video_length, get_topic

YOUTUBE_TOPIC, VIDEO_LENGTH = range(2)


def youtube_conversation():
    youtube_conv = ConversationHandler(
        entry_points=[CommandHandler('youtube', start_youtube)],
        states={
            YOUTUBE_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_logging_middleware(get_topic))],
            VIDEO_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_logging_middleware(get_video_length))],
        },
        fallbacks=[CommandHandler('cancel', request_logging_middleware(cancel))],
    )
    return youtube_conv
