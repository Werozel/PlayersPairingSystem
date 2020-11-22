from globals import db
from src.misc import timestamp
from enum import IntEnum
from flask import abort


class InvitationType(IntEnum):
    FRIEND = 1
    FROM_GROUP = 2
    FROM_EVENT = 3
    TO_GROUP = 4
    TO_EVENT = 5


EVENTS_FROM_USER = [InvitationType.FRIEND, InvitationType.TO_GROUP, InvitationType.TO_EVENT]


class Invitation(db.Model):

    __tablename__ = "invitation"

    # TODO relationship with Users
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    referrer_id = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.TIMESTAMP, nullable=False, default=timestamp())
    expiration_time = db.Column(db.TIMESTAMP, nullable=True)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Invitation: {self.type}, '{self.referrer_id}', '{self.expiration_time}')"

    @staticmethod
    def get_or_404(id: int):
        invitation = Invitation.query.get(id)
        if invitation is None:
            abort(404)
        return invitation

    @staticmethod
    def get_or_none(id: int):
        return Invitation.query.get(id)

    def is_expired(self):
        return self.expiration_time is not None and self.expiration_time > timestamp()

    def get_referrer(self):
        from libs.models.User import User
        from libs.models.Group import Group
        from libs.models.Event import Event
        if self.type in EVENTS_FROM_USER:
            return User.get_or_404(self.referrer_id)
        elif self.type == InvitationType.FROM_GROUP:
            return Group.get_or_404(self.referrer_id)
        elif self.type == InvitationType.FROM_EVENT:
            return Event.get_or_404(self.referrer_id)
        else:
            return None

    def get_recipient(self):
        from libs.models.User import User
        from libs.models.Group import Group
        from libs.models.Event import Event
        if self.type == InvitationType.FRIEND:
            return User.get_or_404(self.recipient_id)
        elif self.type == InvitationType.TO_GROUP:
            return Group.get_or_404(self.recipient_id)
        elif self.type == InvitationType.TO_EVENT:
            return Event.get_or_404(self.recipient_id)
        else:
            return None

    @staticmethod
    def add(type: InvitationType, recipient_id: int, referrer_id: int, expiration_time=None) -> int:
        if len(Invitation.query.filter((Invitation.recipient_id == recipient_id)
                                       & (Invitation.referrer_id == referrer_id)
                                       & (Invitation.type == type)
                                       & ((Invitation.expiration_time == None) | (Invitation.expiration_time > timestamp()))).all()) > 0:
            return -1
        invitation = Invitation(type=type,
                                recipient_id=recipient_id,
                                referrer_id=referrer_id,
                                creation_time=timestamp(),
                                expiration_time=expiration_time)
        db.session.add(invitation)
        db.session.commit()
        return invitation.id

    @staticmethod
    def get_all_for_event(event_id: int) -> list:
        return Invitation.query.filter((Invitation.type == InvitationType.TO_EVENT)
                                       & (Invitation.recipient_id == event_id)
                                       & ((Invitation.expiration_time == None) | (Invitation.expiration_time > timestamp()))).all()

    @staticmethod
    def get_all_for_group(group_id: int) -> list:
        return Invitation.query\
            .filter((Invitation.type == InvitationType.TO_GROUP)
                    & (Invitation.recipient_id == group_id)
                    & ((Invitation.expiration_time == None) | (Invitation.expiration_time > timestamp()))).all()

    def accept(self):
        from libs.models.User import User
        from libs.models.Group import Group
        from libs.models.Event import Event
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
