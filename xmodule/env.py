import os

import dotenv
import pytz
from tzlocal import get_localzone

from xmodule.utils.parser import parse_bool, parse_int

_dotenv_path = dotenv.find_dotenv()
if _dotenv_path == '':
    user_path = os.path.expanduser('~')
    user_env = os.path.join(user_path, '.env')
    if os.path.exists(user_env):
        _dotenv_path = user_env

if _dotenv_path:
    dotenv.load_dotenv(_dotenv_path)


def get(key, default=None):
    return os.getenv(key, default)


def get_int(key, default=None):
    return parse_int(os.getenv(key), default=default)


def get_bool(key, default=None):
    value = os.getenv(key)
    if not value:
        return default

    return parse_bool(value, default=default)


def local_timezone():
    timezone = get('LOCAL_TIMEZONE')
    if timezone is not None:
        return timezone

    try:
        return get_localzone().zone
    except pytz.UnknownTimeZoneError:
        return 'UTC'
