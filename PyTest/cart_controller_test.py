import unittest
from app import create_app, db
from ..Models.user_model import User
from ..Models.laptop_model import Laptop
from ..Models.cart_model import Cart
from ..Models.cart_item_model import CartItem
from ..Models.order_model import Order
import json

class CartControllerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(username="testuser", password="testpassword")
            db.session.add(user)
            db.session.commit()
            laptop = Laptop(name="testlaptop", price=1000)
            db.session.add(laptop)
            db.session.commit()
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()
            cart_item = CartItem(cart_id=cart.id, laptop_id=laptop.id, quantity=1)
            db.session.add(cart_item)
            db.session.commit()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_cart(self):
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            response = self.client.get(f"/api/carts/{user.id}")
            data = json.loads(response.data.decode("utf-8"))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["user_id"], user.id)
    
    def test_add_to_cart(self):
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            laptop = Laptop.query.filter_by(name="testlaptop").first()
            response = self.client.post(f"/api/carts/{user.id}/items", json={"laptop_id": laptop.id, "quantity": 2})
            data = json.loads(response.data.decode("utf-8"))
            self.assertEqual(response.status_code, 201)
            self.assertEqual(len(data["cart_items"]), 2)
    
    def test_remove_from_cart(self):
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            cart = Cart.query.filter_by(user_id=user.id).first()
            cart_item = CartItem.query.filter_by(cart_id=cart.id).first()
            response = self.client.delete(f"/api/carts/{user.id}/items/{cart_item.id}")
            data = json.loads(response.data.decode("utf-8"))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["cart_items"]), 0)
    
    def test_checkout(self):
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            response = self.client.post(f"/api/carts/{user.id}/checkout")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(CartItem.query.all()), 0)
            self.assertEqual(len(Cart.query.all()), 1)
            self.assertEqual(len(Order.query.all()), 1)
            self.assertEqual(Order.query.first().user_id, user.id)
            self.assertEqual(Order.query.first().status, "pending")
