from globals import db


class PlayTime(db.Model):
    __tablename__ = "play_times"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    day_of_week = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    address_id = db.Column(db.BigInteger, db.ForeignKey("address_cache.id"), nullable=True)
    location_id = db.Column(db.BigInteger, db.ForeignKey("location_cache.id"), nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)

    @staticmethod
    def get(id: int):
        return PlayTime.query.filter_by(id=id).first()

    @staticmethod
    def get_all_for_user_id(id: int):
        return PlayTime.query.filter_by(user_id=id).all()
