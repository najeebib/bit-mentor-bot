from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
from bot.config.logging_config import generate_request_id, setup_logger

def request_logging_middleware(handler, *handler_args, **handler_kwargs):
    @wraps(handler)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        try:
            # Generate a unique request ID for this specific request
            request_id = generate_request_id()
            user_info = update.effective_user

            # Handle case where user might not have a username
            if user_info.username:
                username = user_info.username
            else:
                username = "anonymous"

            handler_name = handler.__name__

            # Setup the logger with this request-specific context
            logger = setup_logger(request_id=request_id, user=username, handler_name=handler_name)

            # Log the start of the request handling
            logger.info(f"Handling {handler_name} for user {username} ({user_info.id})")

            # Combine all args and kwargs
            combined_args = handler_args + args
            combined_kwargs = {**handler_kwargs, **kwargs}

            # Call the actual handler
            return handler(update, context, *combined_args, **combined_kwargs)

        except Exception as e:
            logger.error(f"Error in request_logging_middleware for handler {handler_name}: {e}")
            # Optionally, send a message to the user if desired
            if update and update.message:
                update.message.reply_text("An error occurred while processing your request. Please try again later.")
            raise

    return wrapper
