import logging
from libs.Users import User
from globals import connection
from constants.requests import get_group, delete_group, update_group, upload_group


class Group:

    @staticmethod
    def get_valid_id() -> int:
        cursor = connection.cursor()
        cursor.execute("select max(id) from groups")
        data = cursor.fetchone()[0]
        cursor.close()
        return data + 1 if data is not None else 0

    def __init__(self, id: int = None, admin: User = None, sport: str = "", members: list = (),
                 name: str = ""):
        self.sport = sport
        self.admin = admin
        members = list(members)
        self.members = members
        self.name = name
        self.id = int(id) if id is not None else Group.get_valid_id()

    def is_member(self, user) -> bool:
        if isinstance(user, int):
            for m in self.members:
                if m.id == user:
                    return True
        elif isinstance(user, User):
            for m in self.members:
                if m.id == user.id:
                    return True
        return False

    def add_users(self, users) -> None:
        if not self.is_member(users):
            if isinstance(users, int):
                self.members.append(User.get(users))
            if isinstance(users, User):
                self.members.append(users)
        elif isinstance(users, list):
            for u in users:
                if not self.is_member(users):
                    if isinstance(users, int):
                        self.members.append(User.get(u))
                    if isinstance(users, User):
                        self.members.append(u)

    @staticmethod
    def get(id: int):     # Достает группу с id из бд
        cursor = connection.cursor()
        cursor.execute(get_group, [id])
        data = cursor.fetchone()
        cursor.close()
        if data:
            return Group(id=data[0], admin=User.get(data[1]), sport=data[2],
                         members=[User.get(i) for i in data[3]], name=data[4])
        else:
            return None

    def upload(self):  # Загружает и обновляет текущую группу в бд
        cursor = connection.cursor()
        group = Group.get(self.id)
        if group:
            cursor.execute(update_group, [self.admin.id, self.sport, [i.id for i in self.members], self.name, self.id])
        else:
            cursor.execute(upload_group, [self.id, self.admin.id, self.sport, [i.id for i in self.members], self.name])
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
        cursor.execute(delete_group, [id])
        cursor.close()

    def tuple(self) -> tuple:
        return self.id, self.name, str(self.admin.name + " " + self.admin.last_name), \
               self.sport, [i.name + " " + i.last_name for i in self.members]

    def print(self) -> None:
        s = "ID = {0}\n".format(self.id)
        s += "Name = {0}\n".format(self.name)
        s += "Admin = {0}\n".format(self.admin.name + " " + self.admin.last_name)
        s += "Sport = {0}\n".format(self.sport)
        s += "Members = {0}\n".format([i.name + " " + i.last_name for i in self.members])
        print(s)

    def check(self) -> bool:
        if self.id is None or not self.admin or not self.sport or not self.members:
            return False
        else:
            return True


