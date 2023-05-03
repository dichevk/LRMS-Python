from flask import Blueprint, request, jsonify
from app import db
import paypal
from ..Models.order_model import Order
from ..Models.order_item_model import OrderItem

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(user_id=data['user_id'], laptop_id=data['laptop_id'], quantity=data['quantity'], total_price=data['total_price'])
    db.session.add(order)
    db.session.commit()
     # call PayPal API to process payment
    paypal_api = paypal.PayPalAPI()
    payment = paypal_api.process_payment(order.total_amount)

    # update order status based on payment status
    if payment.success:
        order.status = 'PAID'
    else:
        order.status = 'PAYMENT_FAILED'
        
    # second call to update the status in the db
    db.session.commit()
    # return order information in response
    return jsonify(order.serialize()), 201

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
@order_bp.route('/<int:order_id>/order_items', methods=['POST'])
def create_order_item(order_id):
    data = request.get_json()
    order = Order.query.get(order_id)
    if not order:
        return {"error": "Order not found."}, 404
    order_item = OrderItem(order_id=order_id, laptop_id=data['laptop_id'], quantity=data['quantity'])
    db.session.add(order_item)
    db.session.commit()
    return jsonify(order_item.to_dict()), 201

@order_bp.route('/<int:order_id>/order_items/<int:id>', methods=['GET'])
def get_order_item(order_id, id):
    order_item = OrderItem.query.filter_by(order_id=order_id, id=id).first()
    if not order_item:
        return {"error": "Order item not found."}, 404
    return jsonify(order_item.to_dict())

@order_bp.route('/<int:order_id>/order_items', methods=['GET'])
def get_all_order_items(order_id):
    order = Order.query.get(order_id)
    if not order:
        return {"error": "Order not found."}, 404
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    return jsonify([order_item.to_dict() for order_item in order_items])

@order_bp.route('/<int:order_id>/order_items/<int:id>', methods=['PUT'])
def update_order_item(order_id, id):
    order_item = OrderItem.query.filter_by(order_id=order_id, id=id).first()
    if not order_item:
        return {"error": "Order item not found."}, 404
    data = request.get_json()
    order_item.laptop_id = data['laptop_id']
    order_item.quantity = data['quantity']
    db.session.commit()
    return jsonify(order_item.to_dict())