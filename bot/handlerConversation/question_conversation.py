from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

from bot.handlers.basic_handlers import cancel
from bot.handlers.question_handlers import question_command, difficulty_response, answers_response, topic_response
from bot.handlers.user_handlers import user_answer_response
DIFFICULTY, ANSWERS, TOPIC, USER_ANSWER = range(4)


def question_conversation():
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
    return conv_handler