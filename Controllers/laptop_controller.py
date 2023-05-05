from flask import Blueprint, jsonify, request, flash, url_for, redirect, abort, render_template
from app import db
from ..Models.laptop_model import Laptop

laptop_bp = Blueprint('laptop', __name__)

# Controller for the home page
@laptop_bp.route('/')
def index():
    laptops = Laptop.query.all()
    return render_template('index.html', laptops=laptops)

@laptop_bp.route('/laptops', methods=['GET'])
def get_all_laptops():
    laptops = Laptop.query.all()
    return jsonify([laptop.to_dict() for laptop in laptops])

# Controller for a single laptop page
@laptop_bp.route('/<int:id>/template', methods=['GET'])
def get_laptop_template(id):
    laptop = Laptop.query.filter_by(id=id).first()
    if laptop is None:
        abort(404)
    return render_template('laptop.html', laptop=laptop)

@laptop_bp.route('/<int:id>', methods=['GET'])
def get_laptop(id):
    laptop = Laptop.query.get(id)
    if not laptop:
        return {"error": "Laptop not found."}, 404
    return jsonify(laptop.to_dict())

# Controller for adding a new laptop
@laptop_bp.route('/<int:id>', methods=['POST'])
def create_laptop():
    name = request.form['name']
    price = request.form['price']
    specs = request.form['specs']
    image_url = request.form['image_url']
    laptop = Laptop(name=name, price=price, specs=specs, image_url=image_url)
    db.session.add(laptop)
    db.session.commit()
    flash('Laptop added successfully.')
    return redirect(url_for('laptop.index'))

@laptop_bp.route('/<int:id>', methods=['PUT'])
def update_laptop(id):
    laptop = Laptop.get_by_id(id)
    if not laptop:
        return {"error": "Laptop not found."}, 404

    if request.content_type != 'application/json':
        return {"error": "Invalid content type. Expected JSON."}, 400

    data = request.get_json()
    if not data:
        return {"error": "No data provided."}, 400

    if 'name' in data:
        laptop.name = data['name']
    if 'image' in data:
        laptop.image = data['image']
    if 'price' in data:
        laptop.price = data['price']
    if 'specs' in data:
        laptop.specs = data['specs']
    
    laptop.save()

    return {"message": "Laptop updated successfully.", "laptop": laptop.to_dict()}, 200

# Controller for deleting an existing laptop
@laptop_bp.route('/delete/<int:id>', methods=['POST'])
def delete_laptop(id):
    laptop = Laptop.query.filter_by(id=id).first()
    if laptop is None:
        abort(404)
    db.session.delete(laptop)
    db.session.commit()
    flash('Laptop deleted successfully.')
    return redirect(url_for('laptop.index'))
