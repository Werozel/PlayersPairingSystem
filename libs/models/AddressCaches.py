from typing import Optional, List

from globals import db


class Address(db.Model):
    __tablename__ = "address_cache"

    id = db.Column(db.BigInteger, primary_key=True)
    full_address = db.Column(db.String(300), nullable=False)
    short_address = db.Column(db.String(300), nullable=True)
    custom_address = db.Column(db.String(300), nullable=True)
    country = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    street = db.Column(db.String, nullable=True)
    building_number = db.Column(db.String, nullable=True)

    address_rel = db.relationship('LocationToAddress', backref='address', lazy=True)
    play_time_rel = db.relationship('PlayTime', backref='address', lazy=True)
    event_play_time_rel = db.relationship('EventPlayTimes', backref='address', lazy=True)

    @staticmethod
    def get(id):
        return Address.query.filter_by(id=id).first()

    @staticmethod
    def get_by_query(query: str) -> list:
        return Address.query.filter(
            Address.full_address.ilike(query) | Address.short_address.ilike(query) | Address.custom_address.ilike(query)
        ).all()

    def get_short_address(self):
        components = []
        if self.street:
            components.append(self.street)
        if self.building_number:
            components.append(self.building_number)
        return ', '.join(components)

    def __repr__(self):
        return self.short_address


class Location(db.Model):
    __tablename__ = "location_cache"

    id = db.Column(db.BigInteger, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    location_rel = db.relationship('LocationToAddress', backref='location', lazy=True)
    play_time_rel = db.relationship('PlayTime', backref='location', lazy=True)
    event_play_time_rel = db.relationship('EventPlayTimes', backref='location', lazy=True)

    @staticmethod
    def get(id):
        return Location.query.filter_by(id=id).first()

    @staticmethod
    def get_by_location(lat, lng):
        return Location.query.filter_by(latitude=lat, longitude=lng).first()


class LocationToAddress(db.Model):
    __tablename__ = "location_to_address"

    address_id = db.Column(db.BigInteger, db.ForeignKey("address_cache.id"),  nullable=False)
    location_id = db.Column(db.BigInteger, db.ForeignKey("location_cache.id"),  nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('address_id', 'location_id'),
    )

    @staticmethod
    def get_address_for_location(lat, lng) -> List[Address]:
        location = Location.get_by_location(lat, lng)
        if location is None:
            return []
        return [x.address for x in LocationToAddress.query.filter_by(location_id=location.id).all()]

    @staticmethod
    def get_location_for_address(query) -> Optional[Location]:
        addresses = Address.get_by_query(query)
        if len(addresses) == 0:
            return None
        return LocationToAddress.query.filter_by(address_id=addresses[0].id).first().location

    @staticmethod
    def get_location_for_address_id(id) -> Optional[Location]:
        loc = LocationToAddress.query.filter_by(address_id=id).first()
        if loc is None:
            return None
        return loc.location
