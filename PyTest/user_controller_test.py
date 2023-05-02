import pytest
from app import create_app, db
from ..Models.user_model import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")
def new_user():
    user = User(username="testuser", email="testuser@example.com", password=generate_password_hash("password"))
    return user

@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app('testing')
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope="module")
def init_database():
    db.create_all()
    yield
    db.drop_all()

def test_new_user(test_client, init_database, new_user):
    response = test_client.post('/user/register', data=dict(
        username="testuser",
        email="testuser@example.com",
        password="password",
        confirm_password="password"
    ), follow_redirects=True)
    assert response.status_code == 200
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == "testuser"

def test_duplicate_username(test_client, init_database, new_user):
    user = User(username="testuser", email="another@example.com", password=generate_password_hash("password"))
    db.session.add(user)
    db.session.commit()

    response = test_client.post('/user/register', data=dict(
        username="testuser",
        email="testuser@example.com",
        password="password",
        confirm_password="password"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Username already exists' in response.data

def test_duplicate_email(test_client, init_database, new_user):
    user = User(username="anotheruser", email="testuser@example.com", password=generate_password_hash("password"))
    db.session.add(user)
    db.session.commit()

    response = test_client.post('/user/register', data=dict(
        username="testuser2",
        email="testuser@example.com",
        password="password",
        confirm_password="password"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Email already exists' in response.data

def test_invalid_email(test_client, init_database, new_user):
    response = test_client.post('/user/register', data=dict(
        username="testuser",
        email="invalidemail",
        password="password",
        confirm_password="password"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email address' in response.data

def test_login(test_client, init_database, new_user):
    response = test_client.post('/user/login', data=dict(
        email="testuser@example.com",
        password="password"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Login successful' in response.data

def test_login_invalid_credentials(test_client, init_database, new_user):
    response = test_client.post('/user/login', data=dict(
        email="testuser@example.com",
        password="invalidpassword"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

