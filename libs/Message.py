from globals import db, timestamp
from libs.User import User
from libs.Chat import Chat
import json


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())
    is_read = db.Column(db.Boolean, default=False)
    content = db.Column(db.JSON, default=json.dumps({'photos': [], 'audios': [], 'videos': [], 'map_pins': []}))

    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'user_id', 'chat_id'),
    )