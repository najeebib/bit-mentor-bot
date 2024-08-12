import requests
import datetime
from bot.setting.config import config
import re

def is_valid_datetime(date_string):
    """
    Checks if a given date string is in a valid datetime format.

    Args:
        date_string (str): The date string to be validated.

    Returns:
        bool: True if the date string is in a valid datetime format, False otherwise.
    """
    pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\s([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$'
    return bool(re.match(pattern, date_string))

def get_timezone(location):
    """
    Retrieves the timezone ID for a given geographical location.

    Args:
        location (tuple): A tuple containing the latitude and longitude of the location.

    Returns:
        str: The timezone ID if the request is successful, otherwise None.
    """
    latitude, longitude = location
    timestamp = int(datetime.datetime.now().timestamp())
    url = f"https://maps.googleapis.com/maps/api/timezone/json?location={latitude},{longitude}&timestamp={timestamp}&key={config.GOOGLE_TIMEZONE}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            return data['timeZoneId']
    return None
