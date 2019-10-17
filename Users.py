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
        return data + 1 if data is not None else 0

    def __init__(self, id = None, name: str = "", last_name: str = "", age: int = 0, gender: str = "",
                 admined_groups: list = (), sport: list = (),
                 login: str = "", psw: str = "", groups: list = ()):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.admined_groups = list(admined_groups)
        self.sport = list(sport)
        self.login = login
        self.psw = psw
        self.groups = list(groups)

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
                        gender=data[4], admined_groups=data[5], sport=data[6],
                        login=data[7], psw=data[8], groups=data[9])
        else:
            return None

    def upload(self) -> None:  # И загружает и обновляет в бд
        if not self.check():
            logging.error("In upload_user, user " + str(self.id) + " not filled")
            return
        cursor = connection.cursor()
        if User.get(self.id):   # Если пользователь существует в бд
            cursor.execute(update_user_req, [self.name, self.last_name, self.age,
                                             self.gender, self.admined_groups, self.sport,
                                             self.login, self.psw, self.groups, self.id])
        else:   # Если пользователя нет в бд
            cursor.execute(upload_user_req, [self.id, self.name, self.last_name,self.age,
                                             self.gender, self.admined_groups, self.sport,
                                             self.login, self.psw, self.groups])
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
            self.gender = tmp.gender
            self.admined_groups = tmp.admined_groups
            self.sport = tmp.sport
            self.login = tmp.login
            self.psw = tmp.psw
            self.groups = tmp.groups
        cursor.close()

    @staticmethod
    def remove(id) -> None:
        cursor = connection.cursor()
        cursor.execute(delete_user_req, [id])
        cursor.close()

    def add_group(self, id):
        if id not in self.groups:
            self.groups.append(id)

    def check(self) -> bool:
        if not self.id or not self.name or not self.last_name or not \
               self.age or not self.gender or not self.login or not self.psw:
            return False
        else:
            return True

    def tuple(self) -> tuple:
        return self.id, self.name, self.last_name, self.age, self.gender, \
               self.admined_groups, self.sport, self.login, self.psw, self.groups

    def print(self) -> None:
        print(self.tuple())
