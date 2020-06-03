from app_config import SECRET_KEY, DB_URL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_socketio import SocketIO
import datetime
import random


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

    return res


exiting = 0
app = get_app(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

socketIO = SocketIO(app)

sessions = {}


def timestamp():
    return datetime.datetime.now()


def get_rand() -> int:
    from libs.Message import Message
    res = random.randint(1, 9223372036854775807 - 1)
    i = 0
    while Message.get(res) is not None:
        res = random.randint(1, 9223372036854775807 - 1)
        i += 1
        if i == 10:
            break
    return res
