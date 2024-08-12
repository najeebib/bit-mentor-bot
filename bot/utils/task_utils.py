import requests
import datetime
from bot.setting.config import config
import re

def is_valid_datetime(date_string):
    pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\s([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$'
    return bool(re.match(pattern, date_string))

def get_timezone(location):
    latitude, longitude = location
    timestamp = int(datetime.datetime.now().timestamp())
    url = f"https://maps.googleapis.com/maps/api/timezone/json?location={latitude},{longitude}&timestamp={timestamp}&key={config.GOOGLE_TIMEZONE}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            return data['timeZoneId']
    return None
