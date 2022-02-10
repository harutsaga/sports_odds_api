from datetime import datetime, date, timedelta
import pytz
from django.conf import settings

def get_current_time_string():
    tz = pytz.timezone(settings.TIME_ZONE)
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    return current_time