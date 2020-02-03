from globals import db


class Member(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    __tablename__ = "members"

    def __repr__(self):
        return f"{self.id}: {self.user_id} -> {self.group_id}"