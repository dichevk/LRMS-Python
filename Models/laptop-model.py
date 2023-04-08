from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    specs = db.Column(db.String(500), nullable=False)

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
        'specs': self.specs
        }
