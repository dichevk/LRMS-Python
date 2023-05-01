from datetime import datetime
from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    laptop_id = db.Column(db.Integer, db.ForeignKey('laptop.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

    def __repr__(self):
        return f"<Order {self.id}>"
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'total_price': self.total_price,
            'order_date': self.order_date,
        }