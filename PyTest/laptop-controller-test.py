from app.models import Laptop
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
