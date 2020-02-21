from globals import db, timestamp
from libs.User import User

class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())

    chat_role_rel = db.relationship('ChatRole', backref='chat', lazy=True)
    chat_member_rel = db.relationship('ChatMember', backref='chat', lazy=True)
    message_rel = db.relationship('Message', backref='chat', lazy=True)


