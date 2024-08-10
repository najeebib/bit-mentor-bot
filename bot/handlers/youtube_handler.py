import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, ContextTypes
from constants import CATEGORIES
from bot.utils.youtube_utils import *

YOUTUBE_TOPIC, VIDEO_LENGTH = range(2)


async def start_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await send_category_selection(update)
    return YOUTUBE_TOPIC


async def send_category_selection(update: Update):
    categories_text = "\n".join(CATEGORIES)
    message_text = f"Please select a topic from the following categories:\n{categories_text}"

    reply_keyboard = [[category] for category in CATEGORIES]
    await update.message.reply_text(
        message_text,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )


async def get_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_topic = update.message.text
    if selected_topic not in CATEGORIES:
        await send_invalid_topic_message(update)
        return YOUTUBE_TOPIC

    context.user_data['topic'] = selected_topic
    await update.message.reply_text("Please enter the video length (short, medium, long):")
    return VIDEO_LENGTH


async def send_invalid_topic_message(update: Update):
    await update.message.reply_text(
        f"'{update.message.text}' is not a valid topic. Please select a topic from the following categories:\n" + "\n".join(
            CATEGORIES)
    )


async def get_video_length(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    video_length = update.message.text
    context.user_data['video_length'] = video_length
    topic = context.user_data.get('topic', "")
    user_id = update.message.from_user.id

    if not is_valid_video_length(video_length):
        await update.message.reply_text("Invalid length. Please enter 'short', 'medium', or 'long':")
        return VIDEO_LENGTH

    await fetch_and_display_video_links(update, topic, video_length)
    return ConversationHandler.END  # End the conversation after processing


async def mark_video_watched_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    topic = context.user_data.get('topic', "")
    video_length = context.user_data.get('video_length', "")

    original_text = query.message.text
    keyboard = query.message.reply_markup.inline_keyboard

    video_index = get_video_index(query.data)
    video_links = extract_video_links(original_text)
    video_url = video_links[video_index].strip()

    if await handle_video_watched(query, video_url, keyboard[video_index][0].text, user_id):
        return

    await update_watch_history(user_id, topic, video_length, video_url)

    new_keyboard = create_new_keyboard(keyboard, video_index)
    await query.edit_message_text(text=original_text, reply_markup=InlineKeyboardMarkup(new_keyboard))
