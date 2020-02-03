from globals import db


class Member(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    __tablename__ = "members"

    __table_args__ = (
        db.UniqueConstraint('user_id', 'group_id', name='unique_record'),
    )

    def __repr__(self):
        return f"{self.id}: {self.user} -> {self.group}"