from flask import Blueprint, request, jsonify
from ..Controllers import (
    user_controller, 
    laptop_controller, 
    cart_controller, 
    order_controller,
    review_controller
)

api_bp = Blueprint('api', __name__, url_prefix='/api')

# User API Endpoints
api_bp.add_url_rule('/user', view_func=user_controller.get_users, methods=['GET'])
api_bp.add_url_rule('/user/<int:id>', view_func=user_controller.get_user, methods=['GET'])
api_bp.add_url_rule('/user', view_func=user_controller.create_user, methods=['POST'])
api_bp.add_url_rule('/user/<int:id>', view_func=user_controller.update_user, methods=['PUT'])
api_bp.add_url_rule('/user/<int:id>', view_func=user_controller.delete_user, methods=['DELETE'])

# Laptop API Endpoints
api_bp.add_url_rule('/laptop', view_func=laptop_controller.get_laptops, methods=['GET'])
api_bp.add_url_rule('/laptop/<int:id>', view_func=laptop_controller.get_laptop, methods=['GET'])
api_bp.add_url_rule('/laptop', view_func=laptop_controller.create_laptop, methods=['POST'])
api_bp.add_url_rule('/laptop/<int:id>', view_func=laptop_controller.update_laptop, methods=['PUT'])
api_bp.add_url_rule('/laptop/<int:id>', view_func=laptop_controller.delete_laptop, methods=['DELETE'])

# Cart API Endpoints
api_bp.add_url_rule('/cart', view_func=cart_controller.get_carts, methods=['GET'])
api_bp.add_url_rule('/cart/<int:id>', view_func=cart_controller.get_cart, methods=['GET'])
api_bp.add_url_rule('/cart', view_func=cart_controller.create_cart, methods=['POST'])
api_bp.add_url_rule('/cart/<int:id>', view_func=cart_controller.update_cart, methods=['PUT'])
api_bp.add_url_rule('/cart/<int:id>', view_func=cart_controller.delete_cart, methods=['DELETE'])

# Order API Endpoints
api_bp.add_url_rule('/order', view_func=order_controller.get_orders, methods=['GET'])
api_bp.add_url_rule('/order/<int:id>', view_func=order_controller.get_order, methods=['GET'])
api_bp.add_url_rule('/order', view_func=order_controller.create_order, methods=['POST'])
api_bp.add_url_rule('/order/<int:id>', view_func=order_controller.update_order, methods=['PUT'])
api_bp.add_url_rule('/order/<int:id>', view_func=order_controller.delete_order, methods=['DELETE'])

# Review API Endpoints
api_bp.add_url_rule('/review/<int:laptop_id>', view_func=review_controller.get_reviews_for_laptop, methods=['GET'])
api_bp.add_url_rule('/review/<int:laptop_id>', view_func=review_controller.create_review, methods=['POST'])
api_bp.add_url_rule('/review/<int:id>', view_func=review_controller.update_review, methods=['PUT'])
api_bp.add_url_rule('/review/<int:id>', view_func=review_controller.delete_review, methods=['DELETE'])
