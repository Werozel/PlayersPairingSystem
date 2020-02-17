from globals import db


class Friend(db.Model):
    __tablename__ = "friends"

    first_id = db.Column(db.INTEGER, db.ForeignKey("users.id"), nullable=False)
    second_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('first_id', 'second_id'),
    )

    @staticmethod
    def add(first_id: int, second_id: int):
        if (second_id < first_id):
            first_id, second_id = second_id, first_id
        record = Friend(first_id=first_id, second_id=second_id)
        db.session.add(record)
        db.session.commit()

    @staticmethod
    def remove(first_id: int, second_id: int):
        if (second_id < first_id):
            first_id, second_id = second_id, first_id
        record = Friend.query.filter_by(first_id=first_id, second_id=second_id).first()
        db.session.remove(record)
        db.session.commit()

    def __repr__(self):
        return f"{self.first_id} <-> {self.second_id}"