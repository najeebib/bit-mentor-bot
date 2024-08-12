from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
from bot.config.logging_config import generate_request_id, setup_logger


def request_logging_middleware(handler, *handler_args, **handler_kwargs):
    @wraps(handler)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        # Generate a unique request ID for this specific request
        request_id = generate_request_id()
        user_info = update.effective_user
        handler_name = handler.__name__

        # Setup the logger with this request-specific context
        logger = setup_logger(request_id=request_id, user=user_info.username, handler_name=handler_name)

        # Log the start of the request handling
        logger.info(f"Handling {handler_name} for user {user_info.username} ({user_info.id})")

        # Combine all args and kwargs
        combined_args = handler_args + args
        combined_kwargs = {**handler_kwargs, **kwargs}

        # Call the actual handler
        return handler(update, context, *combined_args, **combined_kwargs)

    return wrapper
