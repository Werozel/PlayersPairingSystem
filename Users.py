import threading
import logging
from constants import update_user_req, upload_user_req, get_user_req, delete_user_req
from globals import connection


class User:

    global_user_id_lock = threading.Lock()
    global_user_id = 0  # TODO Организовать получение текущего id из таблицы

    def __init__(self, id = None, name: str = "", last_name: str = "", age: int = 0, sex: str = "",
                 admined_groups: list = (), sport: list = ()):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.admined_groups = list(admined_groups)
        self.sport = list(sport)

        if id:
            self.id = int(id)
        else:
            with User.global_user_id_lock:
                User.global_user_id += 1
                self.id = User.global_user_id

    @staticmethod
    def get_user(id: int):  # Достает пользователя с id из бд
        cursor = connection.cursor()
        cursor.execute(get_user_req, [id])
        data = cursor.fetchone()
        cursor.close()
        if len(data) > 0:
            return User(id=data[0], name=data[1], last_name=data[2], age=data[3],
                        sex=data[4], admined_groups=data[5], sport=data[6])
        else:
            return None

    def upload_user(self):  # И загружает и обновляет в бд
        if not self.check():
            logging.error("In upload_user, user " + str(self.id) + " not filled")
            return
        cursor = connection.cursor()
        if User.get_user(self.id):   # Если пользователь существует в бд
            cursor.execute(update_user_req, [self.id, self.name, self.last_name, self.age,
                                             self.sex, self.admined_groups, self.sport])
        else:   # Если пользователя нет в бд
            cursor.execute(upload_user_req, [self.id, self.name, self.last_name,self.age,
                                             self.sex, self.admined_groups, self.sport])
        cursor.close()

    def update_user(self):  # обновляет текущего из бд (нужна?)
        pass

    @staticmethod
    def remove_user(id):
        cursor = connection.cursor()
        cursor.execute(delete_user_req, [id])
        cursor.close()

    def check(self):
        if not self.id or not self.name or not self.last_name or not self.age or not self.sex:
            return False
        else:
            return True
