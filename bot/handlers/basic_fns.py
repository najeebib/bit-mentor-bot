import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from bot.setting.config import config


difficulty_button1 = KeyboardButton("easy")
difficulty_button2 = KeyboardButton("medium")
difficulty_button3 = KeyboardButton("hard")
difficulty_button4 = KeyboardButton("none")
difficulty_keyboard = ReplyKeyboardMarkup([[difficulty_button1, difficulty_button2],[difficulty_button3, difficulty_button4]],
                               resize_keyboard=True, one_time_keyboard=True)

answers_button1 = KeyboardButton("1")
answers_button2 = KeyboardButton("2")
answers_button3 = KeyboardButton("3")
answers_button4 = KeyboardButton("4")
answers_keyboard = ReplyKeyboardMarkup([[answers_button1, answers_button2], [answers_button3, answers_button4]], resize_keyboard=True, one_time_keyboard=True)

DIFFICULTY, ANSWERS, TOPIC, USER_ANSWER = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, public_ip: str) -> None:
    message = f"Hello! This is your bot.\nPublic IP: {public_ip}"
    await update.message.reply_text(message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "To get a question you need to use /question\nYou will be asked to enter the required information\nFirst you "
        "need to enter a difficulty\nThen enter the number of answers\nThen enter the topic")

async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Choose difficulty level:", reply_markup=difficulty_keyboard)
    return DIFFICULTY

async def difficulty_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    difficulty = update.message.text
    if difficulty and difficulty.lower() not in ["easy", "medium", "hard", "none"]:
        await update.message.reply_text("Invalid difficulty. Please choose from the keyboard options.")
        return DIFFICULTY

    context.user_data['difficulty'] = difficulty
    await update.message.reply_text("Enter number of answers:", reply_markup=answers_keyboard)
    return ANSWERS

async def answers_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    num_of_answers = update.message.text
    if num_of_answers not in ["1", "2", "3", "4"]:
        await update.message.reply_text("Invalid number of answers. Please choose from the keyboard options.")
        return ANSWERS

    context.user_data['num_of_answers'] = int(num_of_answers)
    await update.message.reply_text("Enter a topic:")
    return TOPIC

async def topic_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    topic = update.message.text
    context.user_data['topic'] = topic
    difficulty = context.user_data['difficulty']
    num_of_answers = context.user_data['num_of_answers']
    gen_question_req_body = {"difficulty": difficulty, "topic": topic}
    response = None
    if num_of_answers == 1:
        # if the user want an open ended question send request to server that generate an open ended question
        response = requests.post(f"{config.SERVER_URL}/generate-question", json=gen_question_req_body).json()
    else:
        gen_question_req_body["answers_count"] = num_of_answers
        # if the user want a question with multiple answers send request to server that generate a question with multiple answers
        response = requests.post(f"{config.SERVER_URL}/questions/question", json=gen_question_req_body).json()
    # save the response values in user data (asuming that the response keys are the same for both requests)
    question = response["question_text"]
    answers = response["options"]
    context.user_data['question'] = question
    context.user_data['answers'] = answers
    context.user_data["details"] = response["details"]
    context.user_data["correct_answer"] = response["correct_answer"] if "correct_answer" in response else 0

    reply = f"Question: {question}\n"
    if num_of_answers > 1:
        for i in range(num_of_answers):
            reply += f"({i+1}) {answers[i]}.\n"
        options_keyboard = None
        reply += "\nSelect your answer: \n"
        if num_of_answers == 2:
            options_keyboard = [[KeyboardButton("1"), KeyboardButton("2")]]
        elif num_of_answers == 3:
            options_keyboard = [[KeyboardButton("1"), KeyboardButton("2"), KeyboardButton("3")]]
        else:
            options_keyboard = [[KeyboardButton("1"), KeyboardButton("2")], [KeyboardButton("3"), KeyboardButton("4")]]
        await update.message.reply_text(reply, reply_markup=ReplyKeyboardMarkup(options_keyboard, resize_keyboard=True, one_time_keyboard=True))
    else:
        await update.message.reply_text(reply, reply_markup=ReplyKeyboardMarkup(options_keyboard, resize_keyboard=True, one_time_keyboard=True))

    
    
    return USER_ANSWER

async def user_answer_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    num_of_answers = context.user_data['num_of_answers']
    if num_of_answers == 1:
        await update.message.reply_text("This feature is not available for open ended questions.")
    else:
        options = context.user_data['answers'] 
        user_answer = int(update.message.text) - 1
        correct_answer = int(context.user_data['correct_answer'])
        if user_answer == correct_answer:
            await update.message.reply_text("Correct!")
        else:
            await update.message.reply_text("Incorrect. The correct answer is " + options[correct_answer])


    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation canceled.")
    return ConversationHandler.END


async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(f"{config.SERVER_URL}/")
        response.raise_for_status()
        data = response.json()
        await update.message.reply_text(data["message"])
    except requests.RequestException as e:
        await update.message.reply_text(f"Error fetching data: {e}")
