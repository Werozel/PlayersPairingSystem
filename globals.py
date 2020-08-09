from constants.app_config import SECRET_KEY, DB_URL
from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_socketio import SocketIO
import datetime
import random


def get_arg_or_400(arg: str, to_int: bool = False):
    try:
        res = request.args.get(arg)
        if res is None:
            raise ValueError(f"No such argument {arg}")
        return int(res) if to_int else res
    except ValueError:
        abort(400)


def format_time(time) -> str:
    # TODO format time
    return str(time)


def get_app(name: str) -> Flask:
    res = Flask(name)
    res.config['SECRET_KEY'] = SECRET_KEY
    res.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    res.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # add jinja env variables
    res.jinja_env.globals.update(format_time=format_time)
    res.jinja_env.globals.update(len=len)

    return res


app = get_app(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_route'
login_manager.login_message_category = 'warning'

socketIO = SocketIO(app)

sessions = {}


def timestamp():
    return datetime.datetime.now()


def get_rand() -> int:
    from libs.Message import Message
    res = random.randint(1, 9223372036854775807 - 1)
    i = 0
    while Message.has_id(res):
        res = random.randint(1, 9223372036854775807 - 1)
        i += 1
        if i == 10:
            break
    return res


def create_tables():
    from libs.Group import Group
    from libs.GroupMember import GroupMember
    from libs.Friend import Friend
    from libs.Chat import Chat
    from libs.ChatRole import ChatRole
    from libs.ChatMember import ChatMember
    from libs.ChatNotification import ChatNotification
    from libs.Message import Message
    from libs.Event import Event
    from libs.EventMember import EventMember
    from libs.User import User
    db.create_all()
