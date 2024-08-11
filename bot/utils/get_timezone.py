import requests
import datetime
from bot.setting.config import config
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
