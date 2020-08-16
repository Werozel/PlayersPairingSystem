from constants.app_config import SECRET_KEY, DB_URL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_socketio import SocketIO
from libs.SecureAdmin import get_admin
from src.misc import format_time, is_admin


def get_app(name: str) -> Flask:
    res = Flask(name)
    res.config['SECRET_KEY'] = SECRET_KEY
    res.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    res.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # add jinja env variables
    res.jinja_env.globals.update(format_time=format_time)
    res.jinja_env.globals.update(len=len)
    res.jinja_env.globals.update(is_admin=is_admin)

    return res


app = get_app(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_route'
login_manager.login_message_category = 'warning'

socketIO = SocketIO(app)

admin = get_admin(app, db)

sessions = {}


def create_tables():
    # these are necessary imports for db to register
    from libs.models.Chat import Chat
    from libs.models.ChatMember import ChatMember
    from libs.models.ChatNotification import ChatNotification
    from libs.models.Event import Event
    from libs.models.EventMember import EventMember
    from libs.models.Friend import Friend
    from libs.models.Group import Group
    from libs.models.GroupMember import GroupMember
    from libs.models.Invitation import Invitation
    from libs.models.Message import Message
    from libs.models.PlayTimes import PlayTimes
    from libs.models.User import User
    db.create_all()
