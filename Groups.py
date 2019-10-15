import threading
from Users import User


class Groups:

    global_group_id = 0     # TODO организовать получение из таблицы
    global_group_id_lock = threading.Lock

    def __init__(self, sport: str, admin: User, id: str):
        self.sport = sport
        self.admin = admin
        with Groups.global_group_id_lock:
            Groups.global_group_id += 1
            self.id = Groups.global_group_id

