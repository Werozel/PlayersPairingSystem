from globals import db
from src.misc import timestamp
from flask import abort


class ChatNotification(db.Model):
    __tablename__ = 'notifications'

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())

    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'chat_id'),
    )

    def __repr__(self):
        return f"ChatNotification: {self.user}, {self.chat}, time = {self.time}"

    @staticmethod
    def get_or_404(user_id: int, chat_id: int):
        notification = ChatNotification.query.filter_by(user_id=user_id, chat_id=chat_id).first()
        if notification is None:
            abort(404)
        return notification

    @staticmethod
    def get_or_none(user_id: int, chat_id: int):
        return ChatNotification.query.filter_by(user_id=user_id, chat_id=chat_id).first()

    @staticmethod
    def get_notifications(user_id: int):
        return ChatNotification.query.filter_by(user_id=user_id).all()

    @staticmethod
    def remove(user_id: int, chat_id: int):
        ChatNotification.query.filter_by(user_id=user_id, chat_id=chat_id).delete()
        db.session.commit()

    @staticmethod
    def add(user_id: int, chat_id: int):
        if ChatNotification.get_or_none(user_id, chat_id) is None:
            tmp = ChatNotification(user_id=user_id, chat_id=chat_id, time=timestamp())
            db.session.add(tmp)
            db.session.commit()
