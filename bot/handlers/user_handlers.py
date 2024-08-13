import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.config.logging_config import app_logger
from bot.setting.config import config


def check_answer_with_openai(question, user_answer):
    try:
        data = {
            "question": question,
            "user_answer": user_answer
        }
        app_logger.info(f"Sending answer check to OpenAI for question: {question}")
        response = requests.post(f"{config.SERVER_URL}/check_answer", json=data)
        response.raise_for_status()
        result = response.json()
        app_logger.info(f"Received answer check result: {result}")
        return result["is_correct"]
    except requests.RequestException as e:
        app_logger.error(f"Request error during answer check: {e}")
        return False
    except Exception as e:
        app_logger.error(f"Unexpected error during answer check: {e}")
        return False


async def handle_open_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        user_answer = update.message.text
        question_text = context.user_data['questions']
        correct_answer = context.user_data['correct_answer']

        app_logger.info(
            f"User {update.effective_user.username} ({update.effective_user.id}) provided answer: {user_answer} for open question: {question_text}")

        is_correct = check_answer_with_openai(question_text, user_answer)

        if is_correct:
            await update.message.reply_text("Correct!\n")
            app_logger.info("User provided the correct answer.")
        else:
            await update.message.reply_text(f"Wrong! The correct answer is {correct_answer}.\n")
            app_logger.info("User provided an incorrect answer.")

        explanation = f"Explanation:\n{context.user_data['details'][0]}"
        await update.message.reply_text(explanation)
        app_logger.info("Sent explanation to user.")

        return is_correct
    except Exception as e:
        app_logger.error(
            f"Error handling open question for user {update.effective_user.username} ({update.effective_user.id}): {e}")
        await update.message.reply_text("There was an error processing your answer. Please try again later.")
        return False


async def handle_closed_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        user_answer = update.message.text
        correct_answer = context.user_data['correct_answer'] + 1

        app_logger.info(
            f"User {update.effective_user.username} ({update.effective_user.id}) provided answer: {user_answer} for closed question with correct answer: {correct_answer}")

        is_correct = int(user_answer) == correct_answer

        if is_correct:
            await update.message.reply_text("Correct!\n")
            app_logger.info("User provided the correct answer.")
        else:
            await update.message.reply_text(f"Wrong! The correct answer is {correct_answer}.\n")
            app_logger.info("User provided an incorrect answer.")

        explanation = "Explanation:\n"
        for i, exp in enumerate(context.user_data['details']):
            explanation += f"({i + 1}) {exp}.\n"
        await update.message.reply_text(explanation)
        app_logger.info("Sent explanation to user.")

        return is_correct
    except Exception as e:
        app_logger.error(
            f"Error handling closed question for user {update.effective_user.username} ({update.effective_user.id}): {e}")
        await update.message.reply_text("There was an error processing your answer. Please try again later.")
        return False


async def user_answer_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['users'] = []
        user_answer = update.message.text
        user_id = update.message.from_user.id
        user_entry = {'user_id': user_id, 'answer': user_answer}
        context.user_data['users'].append(user_entry)

        app_logger.info(f"User {update.effective_user.username} ({user_id}) provided answer: {user_answer}.")

        if context.user_data['num_of_answers'] == "1":
            is_correct = await handle_open_question(update, context)
        else:
            is_correct = await handle_closed_question(update, context)

        # Save user's answer to MongoDB
        answer_data = {
            'user_id': user_id,
            'topic': context.user_data['topic'],
            'difficulty': context.user_data['difficulty'],
            'is_correct': is_correct
        }

        try:
            save_response = requests.post(f"{config.SERVER_URL}/update-user-stat", json=answer_data)
            save_response.raise_for_status()
            app_logger.info(f"User stats updated successfully for user {user_id}.")
        except requests.RequestException as e:
            app_logger.error(f"Request error when updating user stats for user {user_id}: {e}")

        try:
            response = requests.post(f"{config.SERVER_URL}/insert-question", json=context.user_data)
            response.raise_for_status()
            app_logger.info(f"Question data inserted successfully for user {user_id}.")
        except requests.RequestException as e:
            app_logger.error(f"Request error when inserting question data for user {user_id}: {e}")

        return ConversationHandler.END
    except Exception as e:
        app_logger.error(f"Error in user_answer_response for user {user_id}: {e}")
        await update.message.reply_text("There was an error processing your response. Please try again later.")
        return ConversationHandler.END
