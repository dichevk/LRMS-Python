from app import db
import datetime

class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    laptop_id = db.Column(db.Integer, db.ForeignKey("laptops.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    orders = db.relationship('Order', backref='cart', lazy=True)

    def __repr__(self):
        return f"<Cart {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "laptop_id": self.laptop_id,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "orders":self.orders
        }
