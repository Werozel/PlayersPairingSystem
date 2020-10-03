from globals import db


class PlayLocation(db.Model):
    __tablename__ = "play_location"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    address = db.Column(db.String)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)

    @staticmethod
    def get(id: int):
        return PlayLocation.query.filter_by(id=id).first()

    @staticmethod
    def get_all_for_user(id: int):
        return PlayLocation.query.filter_by(user_id=id).all()
