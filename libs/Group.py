from globals import db
from libs.GroupMember import GroupMember
from libs.Event import Event


class Group(db.Model):

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    members_rel = db.relationship('GroupMember', backref='group', lazy=True)
    chats_rel = db.relationship('Chat', backref='group', lazy=True)
    event_rel = db.relationship('Event', backref='group', lazy=True)

    __tablename__ = "groups"

    def __repr__(self):
        return f"{self.name}: {self.sport}, admin: {self.admin.username};"

    @staticmethod
    def get_by_sport(sport):
        return Group.query.filter_by(sport=sport).all()
    
    @staticmethod
    def get(id):
        return Group.query.get(int(id))

    def get_members(self):
        members = GroupMember.query.filter_by(group_id=self.id).all()
        return [i.user for i in members]

    def add_member(self, user):
        if user.id not in self.members:
            self.members.append(user.id)
            db.session.add(self)
            db.session.commit()

    def get_events(self):
        return Event.query.filter_by(group_id=self.id).all()
