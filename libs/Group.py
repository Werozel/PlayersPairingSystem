from globals import db
from libs.Member import Member


class Group(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    __tablename__ = "groups"

    def __repr__(self):
        return f"{self.name}, {self.sport}, {self.admin_id}, {self.members}"

    @staticmethod
    def get_by_sport(sport):
        return Group.query.filter_by(sport=sport).all()
    
    @staticmethod
    def get(id):
        return Group.query.get(int(id))

    def get_members(self):
        return [i.user for i in Member.query.filter_by(group=self.id).all()]

    def add_member(self, user):
        if user.id not in self.members:
            self.members.append(user.id)
            db.session.add(self)
            db.session.commit()
