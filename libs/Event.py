from globals import db, timestamp
from flask import abort


class Event(db.Model):

    __tablename__ = "events"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    description = db.Column(db.VARCHAR(300), nullable=True)
    sport = db.Column(db.VARCHAR(50), nullable=False)
    group_id = db.Column(db.BigInteger, db.ForeignKey('groups.id'), nullable=True)
    creation_time = db.Column(db.TIMESTAMP, default=timestamp())
    creator_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=True)
    closed = db.Column(db.Boolean, default=False)
    # TODO добавить карту
    # TODO добавить повторы

    event_members_rel = db.relationship('EventMember', backref='event', lazy=True)

    @staticmethod
    def get_or_404(id: int):
        event = Event.query.get(id)
        if event is None:
            abort(404)
        return event

    @staticmethod
    def get_or_none(id: int):
        return Event.query.get(id)

    def add_member(self, user):
        from libs.EventMember import EventMember
        res = EventMember.query.filter_by(event_id=self.id, user_id=user.id).first()
        if res is not None:
            return
        new_member = EventMember(event_id=self.id, user_id=user.id, time=timestamp())
        db.session.add(new_member)
        db.session.commit()

    def get_members(self):
        from libs.EventMember import EventMember
        return [i.user for i in EventMember.query.filter_by(event_id=self.id).all()]

    def remove_member(self, user):
        from libs.EventMember import EventMember
        res = EventMember.query.filter_by(event_id=self.id, user_id=user.id).first()
        if res is not None:
            db.session.delete(res)
            db.session.commit()

    def delete(self):
        from libs.EventMember import EventMember
        if self is None:
            return
        for i in EventMember.query.filter_by(event_id=self.id).all():
            db.session.delete(i)
        db.session.commit()
        db.session.delete(self)
        db.session.commit()
