import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.setting.config import config


def check_answer_with_openai(question, user_answer):
    data = {
        "question": question,
        "user_answer": user_answer
    }
    response = requests.post(f"{config.SERVER_URL}/check_answer", json=data)
    result = response.json()
    return result["is_correct"]


async def handle_open_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_answer = update.message.text
    question_text = context.user_data['question_text']
    is_correct = check_answer_with_openai(question_text, user_answer)
    correct_answer = context.user_data['correct_answer']
    if is_correct:
        await update.message.reply_text("Correct!\n")
    else:
        await update.message.reply_text(f"Wrong! The correct answer is {correct_answer}.\n")
    explanation = f"Explanation:\n{context.user_data['details'][0]}"
    await update.message.reply_text(explanation)
    return is_correct


async def handle_closed_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_answer = update.message.text
    correct_answer = context.user_data['correct_answer'] + 1
    is_correct = int(user_answer) == correct_answer
    if is_correct:
        await update.message.reply_text("Correct!\n")
    else:
        await update.message.reply_text(f"Wrong! The correct answer is {correct_answer}.\n")
    explanation = "Explanation:\n"
    for i, exp in enumerate(context.user_data['details']):
        explanation += f"({i+1}) {exp}.\n"
    await update.message.reply_text(explanation)
    return is_correct


async def user_answer_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['users'] = []
    user_answer = update.message.text
    user_id = update.message.from_user.id
    user_entry = {'user_id': user_id, 'answer': user_answer}
    context.user_data['users'].append(user_entry)
    if context.user_data['num_of_answers'] == "1":
        is_correct = await handle_open_question(update, context)
    else:
        is_correct = await handle_closed_question(update, context)
    answer_data = {
        'user_id': user_id,
        'topic': context.user_data['topic'],
        'difficulty': context.user_data['difficulty'],
        'is_correct': is_correct
    }
    save_response = requests.post(f"{config.SERVER_URL}/update-user-stat", json=answer_data).json()
    response = requests.post(f"{config.SERVER_URL}/insert-question", json=context.user_data)
    return ConversationHandler.END
