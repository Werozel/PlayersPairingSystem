from flask import request, abort
from flask_login import current_user
from flask_babel import format_datetime
from constants.app_config import ADMIN_IDS
from constants.constants import DATETIME_FORMATS
import datetime
import random


def get_cookie(key: str, default):
    res = request.cookies.get(key)
    return res if res is not None else default


def get_arg_or_400(arg: str, to_int: bool = False):
    try:
        res = request.args.get(arg)
        if res is None:
            raise ValueError(f"No such argument {arg}")
        return int(res) if to_int else res
    except ValueError:
        abort(400)


def get_arg_or_none(arg: str, to_int: bool = False):
    try:
        res = request.args.get(arg)
        return int(res) if res and to_int else res
    except ValueError:
        return None


def format_time(dt) -> str:
    dt_format = DATETIME_FORMATS.get(current_user.language)
    if not dt_format:
        return format_datetime(dt, "EEEE, MMM dd, HH:mm").title()
    now = datetime.datetime.now()
    if dt.year == now.year:
        return format_datetime(dt, dt_format[0]).title()
    else:
        return format_datetime(dt, dt_format[1]).title()


def timestamp():
    return datetime.datetime.now()


def get_rand() -> int:
    from libs.models.Message import Message
    res = random.randint(1, 9223372036854775807 - 1)
    i = 0
    while Message.has_id(res):
        res = random.randint(1, 9223372036854775807 - 1)
        i += 1
        if i == 10:
            break
    return res


def is_admin(user=current_user) -> bool:
    return user.is_authenticated and user.id in ADMIN_IDS
