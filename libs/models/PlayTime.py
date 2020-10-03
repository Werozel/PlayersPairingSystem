from globals import db


class PlayTime(db.Model):
    __tablename__ = "play_times"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    address = db.Column(db.String)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)

    @staticmethod
    def get(id: int):
        return PlayTime.query.filter_by(id=id).first()

    @staticmethod
    def get_all_for_user_id(id: int):
        return PlayTime.query.filter_by(user_id=id).all()
