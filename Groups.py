import logging
from Users import User
from globals import connection
from requests import get_group_req, delete_group_req, update_group_req, upload_group_req


class Group:

    @staticmethod
    def get_valid_id() -> int:
        cursor = connection.cursor()
        cursor.execute("select max(id) from groups")
        data = cursor.fetchone()[0]
        cursor.close()
        return data + 1 if data else 0

    def __init__(self, id: int = None, admin: User = None, sport: str = "", members: list = ()):
        self.sport = sport
        self.admin = admin
        self.members = members
        self.id = id if id else Group.get_valid_id()

    @staticmethod
    def get(id: int):     # Достает группу с id из бд
        cursor = connection.cursor()
        cursor.execute(get_group_req, [id])
        data = cursor.fetchone()
        cursor.close()
        if data:
            return Group(id=data[0], admin=User.get(data[1]), sport=data[2], members=[User.get(i) for i in data[3]])
        else:
            return None

    def upload(self):  # Загружает и обновляет текущую группу в бд
        cursor = connection.cursor()
        group = Group.get(self.id)
        if group:
            cursor.execute(update_group_req, [self.admin.id, self.sport, [i.id for i in self.members], self.id])
        else:
            cursor.execute(upload_group_req, [self.id, self.admin.id, self.sport, [i.id for i in self.members]])
        cursor.close()

    def load(self) -> None:  # Обновляет текущую группу из бд
        if not self.id:
            logging.error("In Group.load: id not specified")
            return
        cursor = connection.cursor()
        tmp = Group.get(self.id)
        if tmp:
            self.id = tmp.id
            self.admin = tmp.admin
            self.sport = tmp.sport
            self.members = tmp.members
        cursor.close()

    @staticmethod
    def remove(id):
        cursor = connection.cursor()
        cursor.execute(delete_group_req, [id])
        cursor.close()

    def tuple(self) -> tuple:
        return self.id, self.admin, self.sport, self.members

    def print(self) -> None:
        print(self.tuple())

    def check(self) -> bool:
        if not self.id or not self.admin or not self.sport or not self.members:
            return False
        else:
            return True


