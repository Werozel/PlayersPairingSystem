from globals import db, timestamp


class ChatNotification(db.Model):
    __tablename__ = 'notifications'

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())

    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'chat_id'),
    )

    @staticmethod
    def get(user_id, chat_id):
        return ChatNotification.query.filter_by(user_id=int(user_id), chat_id=int(chat_id)).first()

    @staticmethod
    def get_notifications(user_id):
        return ChatNotification.query.filter_by(user_id=user_id).all()

    @staticmethod
    def remove(user_id, chat_id):
        ChatNotification.query.filter_by(user_id=int(user_id), chat_id=int(chat_id)).delete()
        db.session.commit()

    @staticmethod
    def add(user_id, chat_id):
        if ChatNotification.get(user_id, chat_id) is None:
            tmp = ChatNotification(user_id=int(user_id), chat_id=int(chat_id), time=timestamp())
            db.session.add(tmp)
            db.session.commit()
