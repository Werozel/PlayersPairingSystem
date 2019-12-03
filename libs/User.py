from libs.globals import db


class User(db.Mode):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column
    last_name = db.Column(db.String(40), unique=False, nullable=False)
    age = ""
    gender = ""
    admined_groups = ""
    sport = ""
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    groups = ""
    last_login = ""
    image_file = db.Column(db.String, nullable=False, default='default.jpg')
    
    def __repr__(self):
        return f""
