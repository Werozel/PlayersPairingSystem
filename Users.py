import threading


class User:

    global_user_id_lock = threading.Lock()
    global_user_id = 0  # TODO Организовать получение текущего id из таблицы

    def __init__(self, name: str, last_name: str, age: int, sex: str, sport: list):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.sport = sport
        with User.global_user_id_lock:
            User.global_user_id += 1
            self.id = User.global_user_id




