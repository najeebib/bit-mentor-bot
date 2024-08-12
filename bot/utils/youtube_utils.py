import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


async def update_watch_history(user_id: int, topic: str, video_length: str, video_url: str):
    payload = {
        "user_id": str(user_id),
        "topic": topic,
        "length": video_length,
        "video_url": video_url
    }


    print(payload)

    response = requests.post(
        "http://localhost:8000/youtube/mark_link_watched",
        json=payload
    )
    response.raise_for_status()


async def handle_video_watched(query: Update.callback_query, video_url: str, button_text: str, user_id: int) -> bool:
    if button_text == "Watched":
        print(f"User {user_id} clicked on 'Watched' for: {video_url}")
        await query.message.reply_text("You have already watched this video.")
        return True

    print(f"User {user_id} clicked on: {video_url}")
    await query.message.reply_text(f"You clicked on the video: {video_url}")
    return False


def create_new_keyboard(keyboard: list, video_index: int) -> list:
    new_keyboard = []
    for i in range(len(keyboard)):
        if i == video_index:
            new_keyboard.append([InlineKeyboardButton("Watched", callback_data=f"watch_{i + 1}")])
        else:
            new_keyboard.append([keyboard[i][0]])
    return new_keyboard


def extract_video_links(original_text: str) -> list:
    return original_text.split("\n")[2:]


def get_video_index(callback_data: str) -> int:
    return int(callback_data.split("_")[1]) - 1


def is_valid_video_length(video_length: str) -> bool:
    return video_length in ["short", "medium", "long"]


async def display_video_links(update, video_links: list):
    keyboard = [
        [InlineKeyboardButton(f"Watch video {i + 1}", callback_data=f"watch_{i + 1}")]
        for i in range(len(video_links))
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_text = "Here are the top YouTube videos:\n\n" + "\n".join(video_links)
    await update.message.reply_text(reply_text, reply_markup=reply_markup)


async def fetch_and_display_video_links(update: Update, topic: str, video_length: str):
    try:
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
            return

        await display_video_links(update, video_links)

    except requests.HTTPError as e:
        await update.message.reply_text(f"Error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
