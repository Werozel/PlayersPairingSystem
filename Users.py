import threading
from globals import connection


class User:

    global_user_id_lock = threading.Lock()
    global_user_id = 0  # TODO Организовать получение текущего id из таблицы

    def __init__(self, name: str, last_name: str, age: int, sex: str, sport: list):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.sport = sport
        self.admined_groups = []
        with User.global_user_id_lock:
            User.global_user_id += 1
            self.id = User.global_user_id

    @staticmethod
    def get_user(id: int):  # Достает пользователя с id из бд
        cursor = connection.cursor()
        cursor.execute("select * from users where id = {0}".format(id))
        data = cursor.fetchone()
        print(data)
        cursor.close()

    def upload_user(self):  # И загружает и обновляет в бд
        pass

    def update_user(self):  # обновляет текущего и бд (нужна?)
        pass


