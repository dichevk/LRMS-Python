from flask import Blueprint, render_template, redirect, url_for
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
