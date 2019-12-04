from libs.globals import db, timestamp


class User(db.Mode):

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    members = db.Column(db.ARRAY)
    name = db.Column(db.String(50), nullable=False)