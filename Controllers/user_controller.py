from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from ..Models import db, User
from app import app, db

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required."}), 400

    username = data.get('username')
    password = data.get('password')
    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully.", "user": new_user.to_dict()}), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)

    data = request.json
    if not data:
        return jsonify({"error": "No data provided."}), 400

    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])

    db.session.commit()

    return jsonify({"message": "User updated successfully.", "user": user.to_dict()}), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully."}), 200
