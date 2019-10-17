import threading
from Users import User


class Groups:

    global_group_id = 0     # TODO организовать получение из таблицы
    global_group_id_lock = threading.Lock()

    def __init__(self, sport: str, admin: User):
        self.sport = sport
        self.admin = admin
        self.users = [admin]
        with Groups.global_group_id_lock:
            Groups.global_group_id += 1
            self.id = Groups.global_group_id

    @staticmethod
    def get_group(id: int): # Достает группу с id из бд
        pass

    def upload_group(self): # Загружает и обновляет текущую группу в бд
        pass

    def update_group(self): # Обновляет текущую группу из бд
        pass