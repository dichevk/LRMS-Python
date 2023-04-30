import json
from ..Models.order_model import Order
from ..Models.laptop_model import Laptop
from ..Models.user_model import User

def test_create_order(client, db):
    # Create a test user
    user = User(name='Test User')
    db.session.add(user)
    db.session.commit()

    # Create a test laptop
    laptop = Laptop(name='Test Laptop', price=1000.00, specs='Test Specs')
    db.session.add(laptop)
    db.session.commit()

    # Create a new order
    data = {
        'user_id': user.id,
        'laptop_id': laptop.id,
        'quantity': 1,
        'total_price': 1000.00
    }
    response = client.post('/orders', json=data)

    assert response.status_code == 201
    assert response.json['user_id'] == user.id
    assert response.json['laptop_id'] == laptop.id
    assert response.json['quantity'] == 1
    assert response.json['total_price'] == 1000.00

def test_get_orders(client, db):
    # Create a test user
    user = User(name='Test User')
    db.session.add(user)
    db.session.commit()

    # Create a test laptop
    laptop = Laptop(name='Test Laptop', price=1000.00, specs='Test Specs')
    db.session.add(laptop)
    db.session.commit()

    # Create some test orders
    order1 = Order(user_id=user.id, laptop_id=laptop.id, quantity=1, total_price=1000.00)
    order2 = Order(user_id=user.id, laptop_id=laptop.id, quantity=2, total_price=2000.00)
    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()

    # Get all orders
    response = client.get('/orders')
    assert response.status_code == 200
    assert len(response.json) == 2

    # Get orders for a specific user
    response = client.get(f'/orders?user_id={user.id}')
    assert response.status_code == 200
    assert len(response.json) == 2

    # Get orders for a specific laptop
    response = client.get(f'/orders?laptop_id={laptop.id}')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_order(client, db):
    # Create a test user
    user = User(name='Test User')
    db.session.add(user)
    db.session.commit()

    # Create a test laptop
    laptop = Laptop(name='Test Laptop', price=1000.00, specs='Test Specs')
    db.session.add(laptop)
    db.session.commit()

    # Create a test order
    order = Order(user_id=user.id, laptop_id=laptop.id, quantity=1, total_price=1000.00)
    db.session.add(order)
    db.session.commit()

    # Get the order
    response = client.get(f'/orders/{order.id}')
    assert response.status_code == 200
    assert response.json['user_id'] == user.id
    assert response.json['laptop_id'] == laptop.id
    assert response.json['quantity'] == 1
    assert response.json['total_price'] == 1000.00

def test_update_order(client, db):
    # Create a new order
    order = Order(user_id=1, laptop_id=1, quantity=2, total_price=1000.0)
    db.session.add(order)
    db.session.commit()

    # Update the order
    response = client.put(f'/api/orders/{order.id}', json={
        'quantity': 5,
        'total_price': 2500.0
    })

    assert response.status_code == 200
    assert response.json['id'] == order.id
    assert response.json['user_id'] == order.user_id
    assert response.json['laptop_id'] == order.laptop_id
    assert response.json['quantity'] == 5
    assert response.json['total_price'] == 2500.0