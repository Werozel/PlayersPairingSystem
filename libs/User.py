from globals import db, timestamp, login_manager, app
from libs.Group import Group
from libs.GroupMember import GroupMember
from flask_login import UserMixin, current_user
import secrets
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def set_user_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    picture.save(picture_path)
    current_user.image_file = picture_fn


class User(db.Model, UserMixin):

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(40), nullable=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String, nullable=True)
    sport = db.Column(db.ARRAY(db.String))
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    register_time = db.Column(db.TIMESTAMP, default=timestamp())
    last_login = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())
    image_file = db.Column(db.String, nullable=False, default='default.jpg')

    groups_rel = db.relationship('Group', backref='admin', lazy=True)
    members_rel = db.relationship('GroupMember', backref='user', lazy=True)
    friends_rel_1 = db.relationship('Friend', backref='first', lazy=True, primaryjoin="User.id==Friend.first_id")
    friends_rel_2 = db.relationship('Friend', backref='second', lazy=True, primaryjoin="User.id==Friend.second_id")
    chat_admin_rel = db.relationship('Chat', backref='admin', lazy=True)
    chat_role_rel = db.relationship('ChatRole', backref='user', lazy=True)
    chat_member_rel = db.relationship('ChatMember', backref='user', lazy=True)
    message_rel = db.relationship('Message', backref='user', lazy=True)
    notification_rel = db.relationship('Notification', backref='user', lazy=True)
    event_member_rel = db.relationship('EventMember', backref='user', lazy=True)
    event_rel = db.relationship('Event', backref='user', lazy=True)


    __tablename__ = "users"

    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.last_name}', '{self.email}')"

    @staticmethod
    def get(id: int):
        return User.query.get(int(id))

    def friend_add(self, friend_id: int):
        from libs.Friend import Friend
        Friend.add(self.id, int(friend_id))

    def friend_remove(self, friend_id: int):
        from libs.Friend import Friend
        Friend.remove(self.id, int(friend_id))

    def friends_get(self) -> list:
        from libs.Friend import Friend
        first = Friend.query.filter_by(first_id=self.id).all()
        first_set = set(map(lambda y: User.get(y.second_id), first))
        second = Friend.query.filter_by(second_id=self.id).all()
        second_set = set(map(lambda y: User.get(y.first_id), second))
        return list(first_set.union(second_set))

    def get_groups(self):
        return [i.group for i in GroupMember.query.filter_by(user_id=self.id).all()]

    def get_chats(self):
        from libs.ChatMember import ChatMember
        return list(filter(lambda x: x.deleted is None, [i.chat for i in ChatMember.query.filter(ChatMember.user_id==self.id and
                                                        ChatMember.deleted is None).all()]))

    def get_notifications(self):
        from libs.Notification import Notification
        return [i.chat for i in Notification.get_notifications(self.id)]

    def is_notified(self):
        return len(self.get_notifications()) != 0

    def get_events(self):
        from libs.EventMember import EventMember
        return [i.event for i in EventMember.query.filter_by(user_id=self.id).all()]



