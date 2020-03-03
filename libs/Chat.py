from globals import db, timestamp
from libs.User import User
import copy

class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(100), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())
    last_msg_id = db.Column(db.BIGINT, db.ForeignKey('messages.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True) # is_group
    deleted = db.Column(db.TIMESTAMP, nullable=True, default=None)

    chat_role_rel = db.relationship('ChatRole', backref='chat', lazy=True)
    chat_member_rel = db.relationship('ChatMember', backref='chat', lazy=True)
    message_rel = db.relationship('Message', backref='chat', lazy=True, primaryjoin="Chat.id==Message.chat_id")
    notification_rel = db.relationship('Notification', backref='chat', lazy=True)

    @staticmethod
    def get(id):
        return Chat.query.get(int(id))

    def get_history(self):
        from libs.Message import Message
        return Message.get_history(self.id)

    def get_members(self):
        from libs.ChatMember import ChatMember
        return [i.user for i in ChatMember.query.filter_by(chat_id=self.id, deleted=None).all()]

    def add_member(self, id: int, is_group=True):
        from libs.ChatMember import ChatMember
        if id not in [i.id for i in self.get_members()]:
            new = ChatMember(user_id=id, chat_id=self.id, is_group=is_group, time=timestamp())
            db.session.add(new)
            db.session.commit()

    def update_last_msg(self, message):
        self.last_message = message
        db.session.commit()

    def get_new_messages(self, user_id=None):
        from libs.Message import Message
        if user_id is None:
            return Message.query.filter_by(chat_id=self.id, is_read=False).all()
        else:
            return list(filter(lambda x: x.user_id != user_id, Message.query.filter_by(chat_id=self.id, is_read=False).all()))