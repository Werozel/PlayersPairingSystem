import psycopg2
import config
import logging


exiting = 0

try:
    __connection = psycopg2.connect(user=config.db_user,
                                    password=config.db_psw,
                                    host="127.0.0.1",
                                    port="5432",
                                    database=config.db_name)
    cursor = __connection.cursor()
    print(cursor)
except:
    logging.error("Error while connecting to database")


def finish():
    if __connection:
        cursor.close()
        __connection.close()
