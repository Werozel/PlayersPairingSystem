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