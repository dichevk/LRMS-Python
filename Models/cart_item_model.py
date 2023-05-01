from app import db

class CartItem(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    laptop_id = db.Column(db.Integer, db.ForeignKey("laptops.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<CartItem {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "laptop_id": self.laptop_id,
            "quantity": self.quantity
        }