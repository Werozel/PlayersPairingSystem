from globals import db, timestamp
from flask import abort


class Group(db.Model):

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    closed = db.Column(db.Boolean, default=False)

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
    def get_or_404(id: int):
        group = Group.query.get(id)
        if group is None:
            abort(404)
        return group

    @staticmethod
    def get_or_none(id: int):
        return Group.query.get(id)

    def get_members(self):
        from libs.GroupMember import GroupMember
        members = GroupMember.query.filter_by(group_id=self.id).all()
        return [i.user for i in members]

    def add_member(self, user):
        from libs.GroupMember import GroupMember
        if user.id not in self.get_members():
            new_row = GroupMember(user_id=user.id, group_id=self.id, time=timestamp())
            db.session.add(new_row)
            db.session.commit()

    def get_events(self):
        from libs.Event import Event
        return Event.query.filter_by(group_id=self.id).all()

    def delete(self):
        from libs.GroupMember import GroupMember
        if self is None:
            return
        for e in self.get_events():
            db.sessin.delete(e)
        db.session.commit()
        for i in GroupMember.query.filter_by(group_id=self.id).all():
            db.session.delete(i)
        db.session.commit()
        db.session.delete(self)
        db.session.commit()


