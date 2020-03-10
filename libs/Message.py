from globals import db, timestamp
from libs.User import User
from libs.Chat import Chat
import json


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())
    is_read = db.Column(db.Boolean, default=False)
    content = db.Column(db.JSON, default=json.dumps({'photos': [], 'audios': [], 'videos': [], 'map_pins': []}))
    text = db.Column(db.VARCHAR(1000), default="")

    chat_last_msg_rel = db.relationship('Chat', backref='last_message', lazy=True, primaryjoin="Message.id==Chat.last_msg_id")

    @staticmethod
    def get(id):
        return Message.query.filter_by(id=int(id)).first()

    @staticmethod
    def get_history(chat_id):
        return Message.query.filter_by(chat_id=int(chat_id)).order_by(Message.time).limit(50).all()

    def __repr__(self):
        return f"{self.user.username}: {self.text} || {self.is_read}"