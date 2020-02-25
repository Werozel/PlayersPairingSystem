from globals import db, timestamp
from libs.User import User

class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(100), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())
    last_msg_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)

    chat_role_rel = db.relationship('ChatRole', backref='chat', lazy=True)
    chat_member_rel = db.relationship('ChatMember', backref='chat', lazy=True)
    message_rel = db.relationship('Message', backref='chat', lazy=True, primaryjoin="Chat.id==Message.chat_id")

    @staticmethod
    def get(id):
        return Chat.query.get(int(id))

    def get_history(self):
        from libs.Message import Message
        return Message.get_history(self.id)

    def get_members(self):
        from libs.ChatMember import ChatMember
        return [i.user for i in ChatMember.query.filter_by(chat_id=self.id).all()]

    def add_member(self, id: int, is_group=True):
        from libs.ChatMember import ChatMember
        new = ChatMember(user_id=id, chat_id=self.id, is_group=is_group, time=timestamp())
        db.session.add(new)
        db.session.commit()