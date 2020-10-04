from flask import Flask, g
from flask_babel import Babel, gettext
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import GoogleV3, Nominatim

from constants.app_config import SECRET_KEY, DB_URL
from constants.config import GOOGLE_API
from constants.constants import DayOfWeek
from libs.SecureAdmin import get_admin
from src.address_cache import save_address_cache
from src.misc import format_date_time, is_admin, get_cookie, format_time
from apscheduler.schedulers.background import BackgroundScheduler
from flask_googlemaps import GoogleMaps
import atexit


def get_scheduler() -> BackgroundScheduler:
    res = BackgroundScheduler()
    atexit.register(lambda: res.shutdown())
    return res


def get_app(name: str) -> Flask:
    res = Flask(name)
    res.config['SECRET_KEY'] = SECRET_KEY
    res.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    res.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    res.config['GOOGLEMAPS_KEY'] = GOOGLE_API

    # jinja env variables
    res.jinja_env.globals.update(format_date_time=format_date_time)
    res.jinja_env.globals.update(format_time=format_time)
    res.jinja_env.globals.update(get_day_of_week=DayOfWeek.get_name)
    res.jinja_env.globals.update(len=len)
    res.jinja_env.globals.update(is_admin=is_admin)
    res.jinja_env.globals.update(set=set)
    res.jinja_env.globals.update(get_cookie=get_cookie)

    return res


app = get_app(__name__)

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

google_api = GoogleV3(api_key=GOOGLE_API)
nominatim = Nominatim(user_agent="sport")

login_manager = LoginManager(app)
login_manager.login_view = 'login_route'
login_manager.login_message_category = 'warning'
login_manager.login_message = gettext("Please log in to view this page.")
login_manager.localize_callback = gettext

babel = Babel(app)

socketIO = SocketIO(app)

admin = get_admin(app, db)

sessions = {}

scheduler = get_scheduler()
scheduler.add_job(func=save_address_cache, trigger="interval", seconds=60)
scheduler.start()

google_maps = GoogleMaps(app)


@babel.localeselector
def get_locale():
    return get_cookie('language', 'en')


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


def create_tables():
    # these are necessary imports for db to register
    db.create_all()
