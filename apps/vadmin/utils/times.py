import time
from datetime import timedelta, datetime

import pytz
from django.utils import timezone

EMAIL_FORMAT_DATETIME = "%Y-%m-%d %H:%M %Z%z"


def convert_datetime_to_timestamp(convert_time, is_nano=False):
    if is_nano:
        return time.mktime(convert_time.timetuple()) * 1000
    return time.mktime(convert_time.timetuple())


def convert_datetime_to_string(convert_datetime, format=EMAIL_FORMAT_DATETIME, timezone=pytz.UTC):
    utc_time = convert_datetime.astimezone(timezone)
    return utc_time.strftime(format)


def get_first_day_week(current_time):
    return current_time - timedelta(days=current_time.weekday())


def get_first_day_month(current_time):
    return current_time - timedelta(days=current_time.day - 1)


def convert_timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.get_current_timezone())


def convert_datetime_from_string(convert_string, format_time, timezone=pytz.UTC):
    converted_datetime = datetime.strptime(convert_string, format_time)
    return converted_datetime.astimezone(timezone)
