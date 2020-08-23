from globals import db


class PlayTimes(db.Model):
    __tablename__ = "play_times"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)

    @staticmethod
    def get_all_for_user_id(id: int):
        return PlayTimes.query.filter_by(user_id=id).all()
