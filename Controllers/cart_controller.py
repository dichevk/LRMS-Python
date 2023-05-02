from flask import Blueprint, jsonify, request
from ..Models.order_model import Order
from ..Models.cart_model import Cart 
from ..Models.cart_item_model import CartItem
from ..Models.laptop_model import Laptop
from ..Models.user_model import User
from ..Models.order_item_model import OrderItem
from app import db
import paypalrestsdk
from flask import g, url_for, session
import datetime

cart_bp = Blueprint('cart_bp', __name__, url_prefix='/cart')


@cart_bp.route('/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    # Get the user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()

    # Check if cart exists
    if cart is None:
        return jsonify({'message': 'Cart not found.'}), 404

    # Return the cart items and their associated laptop details
    cart_items = []
    for item in cart.items:
        laptop = Laptop.query.get(item.laptop_id)
        cart_items.append({
            'id': item.id,
            'laptop_id': item.laptop_id,
            'laptop_name': laptop.name,
            'quantity': item.quantity,
            'price': laptop.price,
        })

    return jsonify({'cart': cart_items})


@cart_bp.route('/<int:user_id>', methods=['POST'])
def add_to_cart(user_id):
    data = request.get_json()

    # Check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found.'}), 404

    # Check if laptop exists
    laptop = Laptop.query.get(data['laptop_id'])
    if laptop is None:
        return jsonify({'message': 'Laptop not found.'}), 404

    # Get the user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()

    # If cart does not exist, create a new one
    if cart is None:
        cart = Cart(user_id=user_id)
        db.session.add(cart)

    # Check if laptop is already in the cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, laptop_id=laptop.id).first()
    if cart_item is None:
        # If not, create a new cart item
        cart_item = CartItem(cart_id=cart.id, laptop_id=laptop.id, quantity=data['quantity'])
        db.session.add(cart_item)
    else:
        # If yes, update the quantity of the existing cart item
        cart_item.quantity += data['quantity']

    db.session.commit()

    return jsonify({'message': 'Laptop added to cart.'}), 201


@cart_bp.route('/<int:user_id>/checkout', methods=['POST'])
def checkout(user_id):
    data = request.get_json()

    # Check if user exists
    user = User.query.get(data['user_id'])
    if user is None:
        return jsonify({'message': 'User not found.'}), 404

    # Get the user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()

    # Check if cart exists
    if cart is None:
        return jsonify({'message': 'Cart not found.'}), 404

    # Check if cart is empty
    if len(cart.items) == 0:
        return jsonify({'message': 'Cart is empty.'}), 400

    # TODO: Implement payment processing with PayPal API

    # Clear the cart
    for item in cart.items:
        db.session.delete(item)
    db.session.delete(cart)
    db.session.commit()

    return jsonify({'message': 'Checkout successful.'}), 200

# Endpoint for getting cart items for a specific cart
@cart_bp.route("/<int:cart_id>/items", methods=["GET"])
def get_cart_items(cart_id):
    cart = Cart.query.filter_by(id=cart_id).first()

    if cart:
        cart_items = CartItem.query.filter_by(cart_id=cart_id).all()
        return jsonify([cart_item.to_dict() for cart_item in cart_items]), 200
    else:
        return jsonify({"message": "Cart not found"}), 404


# Endpoint for adding items to a cart
@cart_bp.route("/<int:cart_id>/items", methods=["POST"])
def add_cart_item(cart_id):
    data = request.get_json()

    laptop_id = data.get("laptop_id")
    quantity = data.get("quantity")

    if not laptop_id or not quantity:
        return jsonify({"message": "Laptop ID and quantity are required"}), 400

    cart = Cart.query.filter_by(id=cart_id).first()
    laptop = Laptop.query.filter_by(id=laptop_id).first()

    if not cart:
        return jsonify({"message": "Cart not found"}), 404

    if not laptop:
        return jsonify({"message": "Laptop not found"}), 404

    cart_item = CartItem.query.filter_by(cart_id=cart_id, laptop_id=laptop_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart_id, laptop_id=laptop_id, quantity=quantity)

    db.session.add(cart_item)
    db.session.commit()

    return jsonify(cart_item.to_dict()), 201


# Endpoint for updating a cart item
@cart_bp.route("/<int:cart_id>/items/<int:item_id>", methods=["PUT"])
def update_cart_item(cart_id, item_id):
    data = request.get_json()
    quantity = data.get("quantity")

    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart_id).first()

    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404

    if quantity:
        cart_item.quantity = quantity

    db.session.commit()

    return jsonify(cart_item.to_dict()), 200


# Endpoint for deleting a cart item
@cart_bp.route("/<int:cart_id>/items/<int:item_id>", methods=["DELETE"])
def delete_cart_item(cart_id, item_id):
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart_id).first()

    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Cart item deleted successfully"}), 200

@cart_bp.route("/checkout", methods=["POST"])
def checkout():
    try:
        # Get the current user
        user_id = g.current_user.id

        # Get the cart for the current user
        cart = Cart.query.filter_by(user_id=user_id).first()

        # Create a new order
        order = Order(user_id=user_id, cart_id=cart.id, status="pending", created_at=datetime.utcnow())
        db.session.add(order)

        # Add the cart items to the order
        for cart_item in cart.cart_items:
            order_item = OrderItem(order_id=order.id, laptop_id=cart_item.laptop_id, quantity=cart_item.quantity)
            db.session.add(order_item)

        # Calculate the total amount for the cart items
        total_amount = 0
        for cart_item in cart.cart_items:
            total_amount += cart_item.laptop.price * cart_item.quantity
        
        # Create a PayPal payment object
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": "{:.2f}".format(total_amount),
                    "currency": "USD"
                },
                "description": "Payment for the laptop order."
            }],
            "redirect_urls": {
                "return_url": url_for("cart.execute_payment", _external=True),
                "cancel_url": url_for("cart.cancel_payment", _external=True)
            }
        })
        
        # Attempt to create a PayPal payment
        if payment.create():
            # Store the PayPal payment ID in the session
            session["paypal_payment_id"] = payment.id
            
            # Retrieve the redirect URL from the payment object and return it to the client
            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    # Empty the cart
                    for cart_item in cart.cart_items:
                        db.session.delete(cart_item)
                    db.session.commit()
                    return jsonify({"redirect_url": redirect_url}), 200
        else:
            # If creating the PayPal payment fails, return an error message
            return jsonify({"error": payment.error}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

   
