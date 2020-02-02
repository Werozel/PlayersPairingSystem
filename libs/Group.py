from globals import db


class Group(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    members = db.Column(db.ARRAY(db.Integer))
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

    def add_member(self, user):
        if user.id not in self.members:
            print(self)
            self.members.append(user.id)
            print(self)
            db.session.add(self)
            print(self)
            db.session.commit()
            print(self)
