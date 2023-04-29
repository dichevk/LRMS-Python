from flask import Blueprint, request, jsonify
from app import db
from ..Models import Order

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(user_id=data['user_id'], laptop_id=data['laptop_id'], quantity=data['quantity'], total_price=data['total_price'])
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict())

@order_bp.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return {"error": "Order not found."}, 404
    return jsonify(order.to_dict())

@order_bp.route('/', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@order_bp.route('/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return {"error": "Order not found."}, 404
    data = request.get_json()
    order.quantity = data['quantity']
    order.total_price = data['total_price']
    db.session.commit()
    return jsonify(order.to_dict())

@order_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return {"error": "Order not found."}, 404
    db.session.delete(order)
    db.session.commit()
    return {"message": "Order deleted successfully."}, 200
