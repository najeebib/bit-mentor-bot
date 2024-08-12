from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

from bot.handlers.basic_handlers import cancel
from bot.handlers.task_handlers import task, title_response, start_response, end_response, location_response, auth_code_response

TITLE, START, END, LOCATION, CODE = range(5)


def task_conversation():
    """
    This function generates a ConversationHandler for task-related conversations.
    
    It defines the entry points, states, and fallbacks for the conversation.
        
    Returns:
        ConversationHandler: A ConversationHandler instance for task conversations.
    """
    task_conv = ConversationHandler(
        entry_points=[CommandHandler('task', task)],
        states={
            TITLE: [MessageHandler(filters.TEXT, title_response)],
            START: [MessageHandler(filters.TEXT, start_response)],
            END: [MessageHandler(filters.TEXT, end_response)],
            LOCATION: [MessageHandler(filters.LOCATION, location_response)],
            CODE : [MessageHandler(filters.TEXT, auth_code_response)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    return task_conv
