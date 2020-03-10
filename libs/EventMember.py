from globals import db, timestamp


class EventMember(db.Model):
    __tablename__ = "event_members"

    event_id = db.Column(db.BigInteger, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, default=timestamp())

    __table_args__ = (
        db.PrimaryKeyConstraint('event_id', 'user_id')
    )