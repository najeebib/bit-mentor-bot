import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from bot.setting.config import config
from bot.config.logging_config import app_logger
def get_difficulty_keyboard():
    difficulty_button1 = KeyboardButton("easy")
    difficulty_button2 = KeyboardButton("medium")
    difficulty_button3 = KeyboardButton("hard")
    difficulty_button4 = KeyboardButton("none")
    return ReplyKeyboardMarkup(
        [[difficulty_button1, difficulty_button2], [difficulty_button3, difficulty_button4]], 
        resize_keyboard=True, one_time_keyboard=True
    )

def get_answers_keyboard():
    answers_button1 = KeyboardButton("1")
    answers_button2 = KeyboardButton("2")
    answers_button3 = KeyboardButton("3")
    answers_button4 = KeyboardButton("4")
    return ReplyKeyboardMarkup(
        [[answers_button1, answers_button2], [answers_button3, answers_button4]], 
        resize_keyboard=True, one_time_keyboard=True
    )

DIFFICULTY, ANSWERS, TOPIC, USER_ANSWER = range(4)

async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        app_logger.info(f"User {update.effective_user.username} ({update.effective_user.id}) triggered question command")
        await update.message.reply_text("Choose difficulty level:", reply_markup=get_difficulty_keyboard())
        app_logger.info("Sent difficulty level options to user")
        return DIFFICULTY
    except Exception as e:
        app_logger.error(f"Error in question_command: {e}")
        await update.message.reply_text("There was an error starting the question process. Please try again.")
        return ConversationHandler.END

async def difficulty_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        difficulty = update.message.text
        app_logger.info(f"User {update.effective_user.username} ({update.effective_user.id}) selected difficulty: {difficulty}")

        if difficulty not in ["easy", "medium", "hard", "none"]:
            app_logger.warning(f"User {update.effective_user.username} selected an invalid difficulty: {difficulty}")
            await update.message.reply_text("Invalid difficulty. Please choose from the keyboard options.")
            return DIFFICULTY

        context.user_data['difficulty'] = difficulty
        app_logger.info(f"Saved difficulty '{difficulty}' to user data")
        await update.message.reply_text("Enter number of answers:", reply_markup=get_answers_keyboard())
        app_logger.info("Sent number of answers options to user")
        return ANSWERS
    except Exception as e:
        app_logger.error(f"Error in difficulty_response: {e}")
        await update.message.reply_text("There was an error processing the difficulty. Please try again.")
        return DIFFICULTY

async def answers_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        num_of_answers = update.message.text
        app_logger.info(f"User {update.effective_user.username} ({update.effective_user.id}) selected number of answers: {num_of_answers}")

        if num_of_answers not in ["1", "2", "3", "4"]:
            app_logger.warning(f"User {update.effective_user.username} selected an invalid number of answers: {num_of_answers}")
            await update.message.reply_text("Invalid number of answers. Please choose from the keyboard options.")
            return ANSWERS

        context.user_data['num_of_answers'] = num_of_answers
        app_logger.info(f"Saved number of answers '{num_of_answers}' to user data")
        await update.message.reply_text("Enter a topic:")
        app_logger.info("Asked user to enter a topic")
        return TOPIC
    except Exception as e:
        app_logger.error(f"Error in answers_response: {e}")
        await update.message.reply_text("There was an error processing the number of answers. Please try again.")
        return ANSWERS


async def handle_open_question_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        topic = update.message.text
        difficulty = context.user_data['difficulty']
        app_logger.info(f"Handling open question for topic '{topic}' with difficulty '{difficulty}'")

        response = requests.post(
            f"{config.SERVER_URL}/questions/",
            json={"difficulty": difficulty, "subject": topic}
        ).json()

        app_logger.info(f"Received response for open question: {response}")

        context.user_data['question_text'] = response["question_text"]
        context.user_data['options'] = [response["correct_answer"]]
        context.user_data['correct_answer'] = response["correct_answer"]

        reply = f'Question: {response["question_text"]}\n'
        await update.message.reply_text(reply)
        app_logger.info("Sent open question to user")

        return USER_ANSWER
    except requests.RequestException as e:
        app_logger.error(f"Request error in handle_open_question_topic for topic '{topic}': {e}")
        await update.message.reply_text("There was an error connecting to the server. Please try again.")
        return TOPIC
    except Exception as e:
        app_logger.error(f"Error in handle_open_question_topic for topic '{topic}': {e}")
        await update.message.reply_text("There was an error processing your request. Please try again.")
        return TOPIC


async def handle_closed_question_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        topic = update.message.text
        difficulty = context.user_data['difficulty']
        num_of_answers = context.user_data['num_of_answers']
        app_logger.info(
            f"Handling closed question for topic '{topic}' with difficulty '{difficulty}' and {num_of_answers} answers")

        response = requests.post(
            f"{config.SERVER_URL}/questions/",
            json={"difficulty": difficulty, "subject": topic, "answers_count": num_of_answers}
        ).json()

        app_logger.info(f"Received response for closed question: {response}")

        context.user_data['question_text'] = response["question_text"]
        context.user_data['options'] = response["options"]
        context.user_data['correct_answer'] = response["correct_answer"]
        context.user_data['details'] = response["details"]

        reply = f'Question: {response["question_text"]}\n'
        for i, answer in enumerate(response["options"]):
            reply += f"({i + 1}) {answer}.\n"

        await update.message.reply_text(reply)
        app_logger.info("Sent closed question to user")

        return USER_ANSWER
    except requests.RequestException as e:
        app_logger.error(f"Request error in handle_closed_question_topic for topic '{topic}': {e}")
        await update.message.reply_text("There was an error connecting to the server. Please try again.")
        return TOPIC
    except Exception as e:
        app_logger.error(f"Error in handle_closed_question_topic for topic '{topic}': {e}")
        await update.message.reply_text("There was an error processing your request. Please try again.")
        return TOPIC


async def topic_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        topic = update.message.text
        context.user_data['topic'] = topic
        app_logger.info(f"User {update.effective_user.username} ({update.effective_user.id}) entered topic: {topic}")

        if context.user_data['num_of_answers'] == "1":
            app_logger.info("User selected 1 answer, handling as open question")
            return await handle_open_question_topic(update, context)
        else:
            app_logger.info("User selected more than 1 answer, handling as closed question")
            return await handle_closed_question_topic(update, context)
    except Exception as e:
        app_logger.error(f"Error in topic_response: {e}")
        await update.message.reply_text("There was an error processing your topic. Please try again.")
        return TOPIC