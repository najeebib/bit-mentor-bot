import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from bot.config.logging_config import app_logger


async def update_watch_history(user_id: int, topic: str, video_length: str, video_url: str):
    try:
        payload = {
            "user_id": str(user_id),
            "topic": topic,
            "length": video_length,
            "video_url": video_url
        }

        app_logger.info(f"Updating watch history for user {user_id} with payload: {payload}")

        response = requests.post(
            "http://localhost:8000/youtube/mark_link_watched",
            json=payload
        )
        response.raise_for_status()
        app_logger.info(f"Successfully updated watch history for user {user_id}")
    except requests.HTTPError as e:
        app_logger.error(f"HTTP error while updating watch history for user {user_id}: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        app_logger.error(f"Unexpected error while updating watch history for user {user_id}: {str(e)}")


def create_new_keyboard(keyboard: list, video_index: int) -> list:
    try:
        new_keyboard = []
        for i in range(len(keyboard)):
            if i == video_index:
                new_keyboard.append([InlineKeyboardButton("Watched", callback_data=f"watch_{i + 1}")])
            else:
                new_keyboard.append([keyboard[i][0]])
        app_logger.info(f"Created new keyboard with 'Watched' button at index {video_index}")
        return new_keyboard
    except Exception as e:
        app_logger.error(f"Error creating new keyboard: {str(e)}")
        return keyboard  # Return the original keyboard if something goes wrong

def extract_video_links(original_text: str) -> list:
    try:
        video_links = original_text.split("\n")[2:]
        app_logger.info(f"Extracted video links: {video_links}")
        return video_links
    except Exception as e:
        app_logger.error(f"Error extracting video links: {str(e)}")
        return []

def get_video_index(callback_data: str) -> int:
    try:
        index = int(callback_data.split("_")[1]) - 1
        app_logger.info(f"Extracted video index: {index}")
        return index
    except Exception as e:
        app_logger.error(f"Error getting video index from callback data: {str(e)}")
        return -1  # Return an invalid index if something goes wrong

def is_valid_video_length(video_length: str) -> bool:
    valid_lengths = ["short", "medium", "long"]
    if video_length in valid_lengths:
        app_logger.info(f"Video length '{video_length}' is valid")
        return True
    else:
        app_logger.warning(f"Invalid video length: {video_length}")
        return False

async def display_video_links(update, video_links: list):
    try:
        keyboard = [
            [InlineKeyboardButton(f"Watch video {i + 1}", callback_data=f"watch_{i + 1}")]
            for i in range(len(video_links))
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = "Here are the top YouTube videos:\n\n" + "\n".join(video_links)
        await update.message.reply_text(reply_text, reply_markup=reply_markup)
        app_logger.info("Displayed video links to the user")
    except Exception as e:
        app_logger.error(f"Error displaying video links: {str(e)}")
        await update.message.reply_text("An error occurred while displaying video links. Please try again later.")

async def fetch_and_display_video_links(update: Update, topic: str, video_length: str):
    try:
        app_logger.info(f"Fetching video links for topic '{topic}' with length '{video_length}'")

        # Uncomment to make an actual API request
        # response = requests.get(f"http://localhost:8000/youtube/?topic={topic}&video_length={video_length}")
        # response.raise_for_status()
        # video_links = response.json()

        # Sample video links for testing
        video_links = [
            "https://www.youtube.com/watch?v=fake10",
            "https://www.youtube.com/watch?v=fake7",
            "https://www.youtube.com/watch?v=fake3",
            "https://www.youtube.com/watch?v=fake4",
            "https://www.youtube.com/watch?v=fake5"
        ]

        if not video_links:
            await update.message.reply_text("No videos found.")
            app_logger.info("No videos found for the given criteria.")
            return

        await display_video_links(update, video_links)

    except requests.HTTPError as e:
        app_logger.error(f"HTTP error while fetching video links: {e.response.status_code} - {e.response.text}")
        await update.message.reply_text(f"Error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        app_logger.error(f"Unexpected error while fetching video links: {str(e)}")
        await update.message.reply_text(f"An error occurred: {str(e)}")