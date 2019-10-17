import logging
import threading
from requests import update_user_req, upload_user_req, get_user_req, delete_user_req
from globals import connection


class User:

    @staticmethod
    def get_valid_id() -> int:
        cursor = connection.cursor()
        cursor.execute("select max(id) from users")
        data = cursor.fetchone()[0]
        cursor.close()
        return data + 1

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
            self.id = User.get_valid_id()

    @staticmethod
    def get(id: int):  # Достает пользователя с id из бд
        cursor = connection.cursor()
        cursor.execute(get_user_req, [id])
        data = cursor.fetchone()
        cursor.close()
        if data:
            return User(id=data[0], name=data[1], last_name=data[2], age=data[3],
                        sex=data[4], admined_groups=data[5], sport=data[6])
        else:
            return None

    def upload(self) -> None:  # И загружает и обновляет в бд
        if not self.check():
            logging.error("In upload_user, user " + str(self.id) + " not filled")
            return
        cursor = connection.cursor()
        if User.get(self.id):   # Если пользователь существует в бд
            cursor.execute(update_user_req, [self.name, self.last_name, self.age,
                                             self.sex, self.admined_groups, self.sport, self.id])
        else:   # Если пользователя нет в бд
            cursor.execute(upload_user_req, [self.id, self.name, self.last_name,self.age,
                                             self.sex, self.admined_groups, self.sport])
        cursor.close()

    def load(self) -> None:  # обновляет текущего из бд
        if not self.id:
            logging.error("in User.load user id not specified")
            return
        cursor = connection.cursor()
        tmp = User.get(self.id)
        if tmp:
            self.id = tmp.id
            self.name = tmp.name
            self.last_name = tmp.last_name
            self.age = tmp.age
            self.sex = tmp.sex
            self.admined_groups = tmp.admined_groups
            self.sport = tmp.sport
        cursor.close()

    @staticmethod
    def remove(id) -> None:
        cursor = connection.cursor()
        cursor.execute(delete_user_req, [id])
        cursor.close()

    def check(self) -> bool:
        if not self.id or not self.name or not self.last_name or not self.age or not self.sex:
            return False
        else:
            return True

    def tuple(self) -> tuple:
        return self.id, self.name, self.last_name, self.age, self.sex, self.admined_groups, self.sport

    def print(self) -> None:
        print(self.tuple())
