from libs.globals import db, timestamp


class User(db.Mode):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(40), unique=False, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.CHAR, nullable=False)
    admined_groups = db.Column(db.ARRAY)
    sport = db.Column(db.ARRAY)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # groups = db.Column(db.Integer)
    last_login = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())
    image_file = db.Column(db.String, nullable=False, default='default.jpg')
    groups = db.relationship('Group', backref='id', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.last_name}', '{self.email}')"


