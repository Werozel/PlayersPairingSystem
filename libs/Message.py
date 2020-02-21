from globals import db, timestamp
from libs.User import User
from libs.Chat import Chat
import json


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.BigInteger, nullable=False)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())
    is_read = db.Column(db.Boolean, default=False)
    content = db.Column(db.JSON, default=json.dumps({'photos': [], 'audios': [], 'videos': [], 'map_pins': []}))
    text = db.Column(db.VARCHAR(1000), default="")

    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'user_id', 'chat_id'),
    )

    @staticmethod
    def get(id, chat_id, user_id):
        return Message.query.filter_by(id=int(id), chat_id=int(chat_id), user_id=int(user_id)).first()

    @staticmethod
    def get_history(chat_id):
        return Message.query.filter_by(chat_id=int(chat_id)).all()