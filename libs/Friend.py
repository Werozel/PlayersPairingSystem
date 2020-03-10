from globals import db, timestamp
from libs.User import User


class Friend(db.Model):
    __tablename__ = "friends"

    first_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    second_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())

    __table_args__ = (
        db.PrimaryKeyConstraint('first_id', 'second_id'),
    )

    @staticmethod
    def add(first_id: int, second_id: int):
        if (second_id < first_id):
            first_id, second_id = second_id, first_id
        if Friend.query.filter_by(first_id=first_id, second_id=second_id).first() is not None:
            return
        record = Friend(first_id=first_id, second_id=second_id, time=timestamp())
        db.session.add(record)
        db.session.commit()

    @staticmethod
    def remove(first_id: int, second_id: int):
        if (second_id < first_id):
            first_id, second_id = second_id, first_id
        if Friend.query.filter_by(first_id=first_id, second_id=second_id).first() is None:
            return
        record = Friend.query.filter_by(first_id=first_id, second_id=second_id).first()
        db.session.delete(record)
        db.session.commit()

    def __repr__(self):
        return f"{self.first_id} <-> {self.second_id}"