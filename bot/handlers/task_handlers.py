import os
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, ContextTypes
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import pytz
from constants import SCOPES 
from bot.utils.get_timezone import get_timezone

TITLE, START, END, LOCATION, CODE = range(5)
async def task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("What is the title of your task?")
    return TITLE

async def title_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['title'] = update.message.text
    await update.message.reply_text("Enter the start date of your task? (YYYY-MM-DD HH:MM:SS)")
    return START

async def start_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['start'] = update.message.text
    await update.message.reply_text("Enter the end date of your task? (YYYY-MM-DD HH:MM:SS)")

    return END

async def end_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['end'] = update.message.text
    await update.message.reply_text(
    'Please share your location for timezone information:',
    reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Share Location", request_location=True)]], one_time_keyboard=True)
    )

    return LOCATION

async def location_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_location = update.message.location
    context.user_data['location'] = (user_location.latitude, user_location.longitude)
    timezone_str = get_timezone(context.user_data['location'])

    start_date_str = context.user_data['start']
    end_date_str = context.user_data['end']
    dt_start = datetime.datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    dt_end = datetime.datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")

    timezone = pytz.timezone(timezone_str)
    dt_start = timezone.localize(dt_start)
    dt_end = timezone.localize(dt_end)


    
    flow = InstalledAppFlow.from_client_secrets_file(
        'bot/credentials.json', SCOPES
    )
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    context.user_data['flow'] = flow
    context.user_data['dt_start'] = dt_start
    context.user_data['dt_end'] = dt_end
    context.user_data['timezone_str'] = timezone_str

    await update.message.reply_text(
        "Please visit the following URL to authorize this application and provide the code here:\n" + auth_url
    )

    return CODE

async def auth_code_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    flow = context.user_data['flow']
    dt_start = context.user_data['dt_start']
    dt_end = context.user_data['dt_end']
    timezone_str = context.user_data['timezone_str']
    code = update.message.text

    try:
        flow.fetch_token(code=code)
        creds = flow.credentials

        service = build("calendar", "v3", credentials=creds)

        event = {
            'summary': context.user_data['title'],
            'start': {
                'dateTime': dt_start.isoformat(),
                'timeZone': timezone_str,
            },
            'end': {
                'dateTime': dt_end.isoformat(),
                'timeZone': timezone_str,
            }
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        await update.message.reply_text(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        await update.message.reply_text(f"Failed to create event: {str(e)}")

    return ConversationHandler.END
