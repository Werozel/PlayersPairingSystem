from globals import db, format_time
from flask import abort
from constants.constants import DayOfWeek


class EventPlayTimes(db.Model):
    __tablename__ = "event_play_times"

    id = db.Column(db.BigInteger, primary_key=True)
    day_of_week = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    address_id = db.Column(db.BigInteger, db.ForeignKey("address_cache.id"), nullable=True)
    location_id = db.Column(db.BigInteger, db.ForeignKey("location_cache.id"), nullable=True)
    event_id = db.Column(db.BigInteger, db.ForeignKey("events.id"), nullable=False)

    @staticmethod
    def get_or_404(id: int):
        event_play_time = EventPlayTimes.query.filter_by(id=id).first()
        if event_play_time:
            return event_play_time
        else:
            abort(404)

    @staticmethod
    def get_or_none(id: int):
        return EventPlayTimes.query.filter_by(id=id).first()

    @staticmethod
    def get_all_for_event(id: int):
        return EventPlayTimes.query.filter_by(event_id=id).all()

    def get_time_str(self):
        result: str = ""
        if self.day_of_week:
            result += DayOfWeek.get_name(self.day_of_week)
        if self.start_time:
            if result:
                result += f": "
            result += format_time(self.start_time)
        if self.end_time and result:
            result += f"-{format_time(self.end_time)}"
        return result
