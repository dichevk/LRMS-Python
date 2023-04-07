from flask import render_template, request, flash, url_for, redirect
from flask import abort
from app import app, db
from ..Models import Laptop

# Controller for the home page
@app.route('/')
def index():
    laptops = Laptop.query.all()
    return render_template('index.html', laptops=laptops)

# Controller for a single laptop page
@app.route('/laptop/<int:id>')
def laptop(id):
    laptop = Laptop.query.filter_by(id=id).first()
    if laptop is None:
        abort(404)
    return render_template('laptop.html', laptop=laptop)

# Controller for adding a new laptop
@app.route('/laptop/new', methods=['GET', 'POST'])
def new_laptop():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        specs = request.form['specs']
        image_url = request.form['image_url']
        laptop = Laptop(name=name, price=price, specs=specs, image_url=image_url)
        db.session.add(laptop)
        db.session.commit()
        flash('Laptop added successfully.')
        return redirect(url_for('index'))
    return render_template('new_laptop.html')

# Controller for editing an existing laptop
@app.route('/laptop/edit/<int:id>', methods=['GET', 'POST'])
def edit_laptop(id):
    laptop = Laptop.query.filter_by(id=id).first()
    if laptop is None:
        abort(404)
    if request.method == 'POST':
        laptop.name = request.form['name']
        laptop.price = request.form['price']
        laptop.specs = request.form['specs']
        laptop.image_url = request.form['image_url']
        db.session.commit()
        flash('Laptop updated successfully.')
        return redirect(url_for('laptop', id=id))
    return render_template('edit_laptop.html', laptop=laptop)

# Controller for deleting an existing laptop
@app.route('/laptop/delete/<int:id>', methods=['POST'])
def delete_laptop(id):
    laptop = Laptop.query.filter_by(id=id).first()
    if laptop is None:
        abort(404)
    db.session.delete(laptop)
    db.session.commit()
    flash('Laptop deleted successfully.')
    return redirect(url_for('index'))
