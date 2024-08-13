from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

from bot.handlers.basic_handlers import cancel
from bot.handlers.middleware import request_logging_middleware
from bot.handlers.question_handlers import question_command, difficulty_response, answers_response, topic_response
from bot.handlers.user_handlers import user_answer_response
DIFFICULTY, ANSWERS, TOPIC, USER_ANSWER = range(4)


def question_conversation():
    """
    Handles the conversation flow for the question command.

    Returns:
        ConversationHandler: A conversation handler object that manages the conversation flow.
    """
    conv_handler = ConversationHandler(
                entry_points=[CommandHandler('question', request_logging_middleware(question_command))],
                states={
                    DIFFICULTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_logging_middleware(difficulty_response))],
                    ANSWERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_logging_middleware(answers_response))],
                    TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_logging_middleware(topic_response))],
                    USER_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_logging_middleware(user_answer_response))],
                },
                fallbacks=[CommandHandler('cancel', request_logging_middleware(cancel))],
            )
    return conv_handler
