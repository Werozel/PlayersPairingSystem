import psycopg2
from constants import config
import logging
import datetime

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
