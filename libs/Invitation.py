from globals import db, timestamp, sessions, socketIO
from enum import IntEnum
from libs.User import User
from libs.Group import Group
from libs.Event import Event


class InvitationType(IntEnum):
    FRIEND = 1
    FROM_GROUP = 2
    FROM_EVENT = 3
    TO_GROUP = 4
    TO_EVENT = 5


EVENTS_FROM_USER = [InvitationType.FRIEND, InvitationType.TO_GROUP, InvitationType.TO_EVENT]


class Invitation(db.Model):
    __tablename__ = "invitation"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    referrer_id = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())
    expiration_time = db.Column(db.TIMESTAMP, nullable=True)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Invitation('{self.type}', '{self.referrer_id}', '{self.expiration_time}')"

    @staticmethod
    def get(id: int):
        return Invitation.query.get(int(id))

    def is_expired(self):
        return self.expiration_time is not None and self.expiration_time > timestamp()

    def get_referrer(self):
        if self.type in EVENTS_FROM_USER:
            return User.get(self.referrer_id)
        elif self.type == InvitationType.FROM_GROUP:
            return Group.get(self.referrer_id)
        elif self.type == InvitationType.FROM_EVENT:
            return Event.get(self.referrer_id)
        else:
            return None

    def get_recipient(self):
        if self.type in EVENTS_FROM_USER:
            return User.get(self.recipient_id)
        elif self.type == InvitationType.FROM_GROUP:
            return Group.get(self.recipient_id)
        elif self.type == InvitationType.FROM_EVENT:
            return Event.get(self.recipient_id)
        else:
            return None

    @staticmethod
    def add(type: InvitationType, recipient_id: int, referrer_id: int, expiration_time=None) -> bool:
        if len(Invitation.query.filter(Invitation.recipient_id == recipient_id
                                       and Invitation.referrer_id == referrer_id
                                       and Invitation.type == type
                                       and Invitation.expiration_time > timestamp()).all()) > 0:
            return False
        invitation = Invitation(type=type,
                                recipient_id=recipient_id,
                                referrer_id=referrer_id,
                                creation_time=timestamp(),
                                expiration_time=expiration_time)
        db.session.add(invitation)
        db.session.commit()
        socket_session = sessions.get(recipient_id)
        if type in [InvitationType.FRIEND, InvitationType.FROM_EVENT, InvitationType.FROM_GROUP]:
            socketIO.emit('invitation', '', room=socket_session)
        return True

    def accept(self):
        if self.is_expired():
            pass
        elif self.type == InvitationType.FRIEND:
            referrer: User = self.get_referrer()
            referrer.friend_add(self.recipient_id)
        elif self.type == InvitationType.FROM_GROUP:
            referrer: Group = self.get_referrer()
            recipient: User = self.get_recipient()
            referrer.add_member(recipient)
        elif self.type == InvitationType.FROM_EVENT:
            referrer: Event = self.get_referrer()
            recipient: User = self.get_recipient()
            referrer.add_member(recipient)
        elif self.type == InvitationType.TO_GROUP:
            referrer: User = self.get_referrer()
            recipient: Group = self.get_recipient()
            recipient.add_member(referrer)
        elif self.type == InvitationType.TO_EVENT:
            referrer: User = self.get_referrer()
            recipient: Event = self.get_recipient()
            recipient.add_member(referrer)
        db.session.delete(self)
        db.session.commit()

    def reject(self):
        db.session.delete(self)
        db.session.commit()
