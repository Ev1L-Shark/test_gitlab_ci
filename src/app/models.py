from . import db


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))
    parkings = db.relationship('ClientParking', back_populates='client')

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.surname}, {self.credit_card}, {self.car_number}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)
    clients = db.relationship('ClientParking', back_populates='parking')

    def __repr__(self):
        return f"{self.id}, {self.address}, {self.opened}, {self.count_places}, {self.count_available_places}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    client = db.relationship('Client', back_populates='parkings')
    parking = db.relationship('Parking', back_populates='clients')

    __table_args__ = (
        db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )

    def __repr__(self):
        return f"{self.id}, {self.client_id}, {self.parking_id}, {self.time_in}, {self.time_out}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
