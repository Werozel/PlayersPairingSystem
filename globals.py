import psycopg2
from constants import config
from app_config import SECRET_KEY, DB_URI
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import logging
import datetime


def get_app(name: str) -> Flask:
    res = Flask(name)
    res.config['SECRET_KEY'] = SECRET_KEY
    res.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    res.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return res


exiting = 0
app = get_app(__name__)
bootstrap =  Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)


try:
    connection = psycopg2.connect(user=config.db_user, password=config.db_psw, host="localhost",
                                  port="5432", database=config.db_name)
    connection.set_session(autocommit=True)
    cursor = connection.cursor()

except Exception as e:
    logging.error("Error while connecting to database")
    logging.error(e)


def timestamp():
    return datetime.datetime.now()


def finish():
    if connection:
        connection.close()
