from globals import db, login_manager, app
from src.misc import timestamp
from libs.models.GroupMember import GroupMember
from flask_login import UserMixin, current_user
from src.crop import center_crop
from PIL import Image
from flask import abort, request
import secrets
import os
import numpy as np


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        user.last_login_ip = request.remote_addr
        db.session.add(user)
        db.session.commit()
    return user


def set_user_picture(picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    picture_path_tmp = picture_path + "-tmp"
    picture.save(picture_path_tmp)
    image = Image.open(picture_path_tmp)
    Image.fromarray(center_crop(np.array(image))).save(picture_path)
    os.remove(picture_path_tmp)
    current_user.image_file = picture_fn


class User(db.Model, UserMixin):

    # from libs.Group import Group
    # from libs.GroupMember import GroupMember
    from libs.models.Friend import Friend
    from libs.models.Chat import Chat
    from libs.models.EventMember import EventMember
    from libs.models.PlayTime import PlayTime
    from libs.models.UserVideos import UserVideos
    # from libs.ChatMember import ChatMember
    # from libs.ChatNotification import ChatNotification
    # from libs.Message import Message
    # from libs.Event import Event
    # from libs.EventMember import EventMember

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
    last_login_ip = db.Column(db.String)
    language = db.Column(db.String, nullable=False, default="en")
    city = db.Column(db.String(50), nullable=True)

    groups_rel = db.relationship('Group', backref='admin', lazy=True)
    members_rel = db.relationship('GroupMember', backref='user', lazy=True)
    friends_rel_1 = db.relationship('Friend', backref='first', lazy=True, primaryjoin="User.id==Friend.first_id")
    friends_rel_2 = db.relationship('Friend', backref='second', lazy=True, primaryjoin="User.id==Friend.second_id")
    chat_admin_rel = db.relationship('Chat', backref='admin', lazy=True)
    chat_member_rel = db.relationship('ChatMember', backref='user', lazy=True)
    message_rel = db.relationship('Message', backref='user', lazy=True)
    notification_rel = db.relationship('ChatNotification', backref='user', lazy=True)
    event_member_rel = db.relationship('EventMember', backref='user', lazy=True)
    event_rel = db.relationship('Event', backref='creator', lazy=True)
    play_time_rel = db.relationship('PlayTime', backref='user', lazy=True)
    user_sport_videos_rel = db.relationship('UserVideos', backref='user', lazy=True)

    __tablename__ = "users"

    def __repr__(self):
        return f"User {self.id}: {self.username}, {self.name}, {self.last_name}, {self.gender})"

    @staticmethod
    def get_or_404(id: int):
        user = User.query.get(int(id))
        if user is None:
            abort(404)
        return user

    @staticmethod
    def get_or_none(id: int):
        return User.query.get(int(id))

    def friend_add(self, friend_id: int):
        from libs.models.Friend import Friend
        Friend.add(self.id, int(friend_id))

    def friend_remove(self, friend_id: int):
        from libs.models.Friend import Friend
        Friend.remove(self.id, int(friend_id))

    def friends_get(self) -> list:
        from libs.models.Friend import Friend
        first = Friend.query.filter_by(first_id=self.id).all()
        first_set = set(map(lambda y: User.get_or_none(y.second_id), first))
        second = Friend.query.filter_by(second_id=self.id).all()
        second_set = set(map(lambda y: User.get_or_none(y.first_id), second))
        return list(first_set.union(second_set))

    def get_groups(self):
        return [i.group for i in GroupMember.query.filter_by(user_id=self.id).all()]

    def get_chats(self):
        from libs.models.ChatMember import ChatMember
        return list(filter(lambda x: x.deleted is None,
                           [i.chat for i in ChatMember.query.filter(ChatMember.user_id == self.id
                                                                    and ChatMember.deleted is None).all()]
                           ))

    def get_notifications(self):
        from libs.models.ChatNotification import ChatNotification
        return [i.chat for i in ChatNotification.get_notifications(self.id)]

    def is_notified(self):
        return len(self.get_notifications()) != 0

    def get_events(self):
        from libs.models.EventMember import EventMember
        return [i.event for i in EventMember.query.filter_by(user_id=self.id).all()]

    def get_invitations(self):
        from libs.models.Invitation import Invitation
        return Invitation.query.filter_by(recipient_id=self.id).all()

    def has_invitations(self):
        return len(list(filter(lambda i: not i.read, self.get_invitations()))) > 0
