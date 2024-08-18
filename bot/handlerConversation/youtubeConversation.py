from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

from bot.handlers.basic_handlers import cancel
from bot.handlers.middleware import request_logging_middleware
from bot.handlers.youtube_handler import start_youtube, get_video_length, get_topic
from bot.config.logging_config import app_logger

YOUTUBE_TOPIC, VIDEO_LENGTH = range(2)


def youtube_conversation():
    """
    This function generates a ConversationHandler for youtube-related conversations.

    It defines the entry points, states, and fallbacks for the conversation.

    Returns:
        ConversationHandler: A ConversationHandler instance for youtube conversations.
    """
    youtube_conv = ConversationHandler(
        entry_points=[CommandHandler('youtube', start_youtube)],
        states={
            YOUTUBE_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_logging_middleware(get_topic))],
            VIDEO_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_logging_middleware(get_video_length))],
        },
        fallbacks=[CommandHandler('cancel', request_logging_middleware(cancel))],
    )
    app_logger.info("Youtube conversation handler created")
    return youtube_conv
