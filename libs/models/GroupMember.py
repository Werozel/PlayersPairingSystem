from globals import db
from src.misc import timestamp


class GroupMember(db.Model):

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.BigInteger, db.ForeignKey('groups.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())

    __tablename__ = "group_members"

    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'group_id'),
    )

    def __repr__(self):
        return f"GroupMember: {self.user} -> {self.group}"
