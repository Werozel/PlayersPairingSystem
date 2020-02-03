from globals import db, timestamp, login_manager, app
from libs.Group import Group
from libs.Member import Member
from flask_login import UserMixin, current_user
from flask import url_for
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(40), nullable=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String, nullable=True)
    sport = db.Column(db.ARRAY(db.String))
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    last_login = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())
    image_file = db.Column(db.String, nullable=False, default='default.jpg')
    groups_rel = db.relationship('Group', backref='admin', lazy=True)
    members_rel = db.relationship('Member', backref='user', lazy=True)

    __tablename__ = "users"

    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.last_name}', '{self.email}')"

    @staticmethod
    def get(id):
        return User.query.get(int(id))

    def get_groups(self):
        return [i.group for i in Member.query.filter_by(user_id=self.id).all()]


