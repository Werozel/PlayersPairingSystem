from globals import db
import json


class ChatRole(db.Model):

    __tablename__ = 'chat_roles'

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id'), nullable=False)
    roles = db.Column(db.JSON, default=json.dumps({}))

    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'chat_id'),
    )
