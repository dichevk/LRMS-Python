from ..Models import Laptop
import app
from app import db
from flask import url_for
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_laptop(client):
    laptop = Laptop(name='Laptop1', price=1000, specs='Specs', image_url='https://example.com/image.jpg')
    db.session.add(laptop)
    db.session.commit()
    response = client.get(url_for('laptop', id=laptop.id))
    assert response.status_code == 200

def test_new_laptop(client):
    response = client.post('/laptop/new', data={'name': 'Laptop2', 'price': 2000, 'specs': 'Specs', 'image_url': 'https://example.com/image2.jpg'})
    assert response.status_code == 302
    assert Laptop.query.filter_by(name='Laptop2').first() is not None

def test_edit_laptop(client):
    laptop = Laptop(name='Laptop3', price=3000, specs='Specs', image_url='https://example.com/image3.jpg')
    db.session.add(laptop)
    db.session.commit()
    response = client.post(url_for('edit_laptop', id=laptop.id), data={'name': 'Laptop4', 'price': 4000, 'specs': 'Specs', 'image_url': 'https://example.com/image4.jpg'})
    assert response.status_code == 302
    assert Laptop.query.filter_by(name='Laptop4').first() is not None

def test_delete_laptop(client):
    laptop = Laptop(name='Laptop5', price=5000, specs='Specs', image_url='https://example.com/image5.jpg')
    db.session.add(laptop)
    db.session.commit()
    response = client.post(url_for('delete_laptop', id=laptop.id))
    assert response.status_code == 302
    assert Laptop.query.filter_by(name='Laptop5').first() is None

def test_update_laptop(client):
    # Create a new laptop
    laptop = {'name': 'MacBook Pro', 'image': 'macbook.jpg', 'price': 1500, 'specs': '16GB RAM, 512GB SSD'}
    response = client.post('/add_laptop', data=laptop)
    assert response.status_code == 302  # Check that the laptop was created successfully

    # Update the laptop
    new_laptop = {'name': 'MacBook Air', 'image': 'macbook-air.jpg', 'price': 1200, 'specs': '8GB RAM, 256GB SSD'}
    response = client.put(f'/laptop/{response.json["laptop"]["id"]}', json=new_laptop)

    assert response.status_code == 200  # Check that the laptop was updated successfully
    assert response.json['message'] == 'Laptop updated successfully.'

    # Fetch the updated laptop and check that it matches the updated data
    response = client.get(f'/laptop/{response.json["laptop"]["id"]}')
    updated_laptop = response.json['laptop']

    assert updated_laptop['name'] == new_laptop['name']
    assert updated_laptop['image'] == new_laptop['image']
    assert updated_laptop['price'] == new_laptop['price']
    assert updated_laptop['specs'] == new_laptop['specs']
