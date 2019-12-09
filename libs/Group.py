from globals import db


class Group(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    members = db.Column(db.ARRAY(db.Integer))
    name = db.Column(db.String(50), nullable=False)

    __tablename__ = "groups"

    def __repr__(self):
        return f"{self.name}, {self.admin_id}, {self.members}"