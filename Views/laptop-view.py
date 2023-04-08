from flask import Blueprint, render_template, redirect, request, url_for
from ..Models import Laptop

bp = Blueprint('laptop', __name__)

@bp.route('/')
def index():
    laptops = Laptop.get_all()
    return render_template('index.html', laptops=laptops)

@bp.route('/laptop/<int:id>')
def laptop(id):
    laptop = Laptop.get_by_id(id)
    return render_template('laptop.html', laptop=laptop)

@bp.route('/add_laptop', methods=['GET', 'POST'])
def add_laptop():
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        price = request.form['price']
        specs = request.form['specs']
        laptop = Laptop(name=name, image=image, price=price, specs=specs)
        laptop.save()
        return redirect(url_for('laptop.index'))
    return render_template('add_laptop.html')

@bp.route('/laptop/<int:id>', methods=['PUT'])
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
