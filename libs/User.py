from globals import db, timestamp


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(40), unique=False, nullable=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.CHAR, nullable=True)
    admined_groups = db.Column(db.ARRAY(db.Integer))
    sport = db.Column(db.ARRAY(db.String))
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    groups = db.Column(db.ARRAY(db.INTEGER))
    last_login = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())
    image_file = db.Column(db.String, nullable=False, default='https://catking.in/wp-content/uploads/2017/02/default-profile-1.png')
    groups_rel = db.relationship('Group', backref='admin', lazy=True)

    __tablename__ = "users"

    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.last_name}', '{self.email}')"

