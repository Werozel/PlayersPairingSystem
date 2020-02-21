from globals import db, timestamp
from libs.User import User
from libs.Chat import Chat


class ChatMember(db.Model):
    __tablename__ = 'chat_members'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())
    is_group = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'chat_id'),
    )


    @staticmethod
    def get_private_chat(first_id, second_id):
        first_id = int(first_id)
        second_id = int(second_id)
        first_chats = set(ChatMember.query.filter_by(user_id=first_id, is_group=False).all())
        second_chats = set(ChatMember.query.filter_by(user_id=second_id, is_group=False).all())
        chat = list(first_chats.intersection(second_chats))
        if len(chat) > 1:
            return chat
        elif len(chat) == 1:
            return chat[0]
        else:
            return None