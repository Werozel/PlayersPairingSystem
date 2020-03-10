from globals import db

class Event(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
