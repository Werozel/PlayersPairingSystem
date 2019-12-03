import psycopg2
from constants import config
from flask import Flask
from app_config import *
from flask_sqlalchemy import SQLAlchemy
import logging
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'jdbc:postgresql://localhost:5432/sport'

db = SQLAlchemy(app)

exiting = 0

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
