from flask import request, abort
from flask_login import current_user
from constants.app_config import ADMIN_IDS
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


def format_time(time) -> str:
    # TODO format time
    return str(time)


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
