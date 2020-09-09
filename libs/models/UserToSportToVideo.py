from globals import db


class UserToSportToVideo(db.Model):
    __tablename__ = "user_sport_videos"

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    sport = db.Column(db.String, nullable=False)
    video_id = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'sport'),
    )

    @staticmethod
    def get_all_for_user_id(user_id: int) -> dict:
        return {i.sport: i.video_id for i in UserToSportToVideo.query.filter_by(user_id=user_id).all()}

    @staticmethod
    def get_video(user_id: int, sport: str) -> str:
        return UserToSportToVideo.query.filter_by(user_id=user_id, sport=sport).first()

    def __repr__(self) -> str:
        return f"UserToSportToVideo: user = {self.user}, sport = {self.sport}, video_id = {self.video_id}"
