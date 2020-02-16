from globals import db, timestamp


class Member(db.Model):

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())

    __tablename__ = "members"

    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'group_id'),
    )

    def __repr__(self):
        return f"{self.id}: {self.user} -> {self.group}"