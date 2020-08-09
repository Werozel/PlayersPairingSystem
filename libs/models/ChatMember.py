from globals import db
from src.misc import timestamp


class ChatMember(db.Model):

    __tablename__ = 'chat_members'

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())
    is_group = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.TIMESTAMP, default=None)

    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'chat_id'),
    )

    def __eq__(self, other):
        return self.user_id == other.user_id and self.chat_id == other.chat_id

    def __repr__(self):
        return f"ChatMember: {self.user}, {self.chat}"

    @staticmethod
    def get_private_chat(first_id, second_id):
        first_id = int(first_id)
        second_id = int(second_id)
        first_chats = ChatMember.query.filter_by(user_id=first_id, is_group=False).all()
        second_chats = ChatMember.query.filter_by(user_id=second_id, is_group=False).all()
        chat = []
        for i in first_chats:
            for j in second_chats:
                if i.chat_id == j.chat_id:
                    chat.append(i)
        if len(chat) > 1:
            return chat
        elif len(chat) == 1:
            return chat[0].chat
        else:
            return None

    @staticmethod
    def get_user_chats(user_id):
        user_id = int(user_id)
        return [i.chat for i in list(filter(lambda x: x.deleted is None or (x.chat.last_message is not None and
                                                                            x.deleted < x.chat.last_message.time),
                                            ChatMember.query.filter_by(user_id=user_id).all()))]
