from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    specs = db.Column(db.String(500), nullable=False)
    availability_start_date = db.Column(db.Date, nullable=False)
    availability_end_date = db.Column(db.Date, nullable=True)
    available = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, image, price, specs, availability_start_date, availability_end_date=None, available=True):
        self.name = name
        self.image = image
        self.price = price
        self.specs = specs
        self.availability_start_date = availability_start_date
        self.availability_end_date = availability_end_date
        self.available = available
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
        'id': self.id,
        'name': self.name,
        'image': self.image,
        'price': self.price,
        'specs': self.specs,
        'availability_start_date':self.availability_start_date,
        'availability_end_date':self.availability_end_date,
        'available':self.available
        }
    