from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .Controllers.cart_controller import cart_bp
from .Controllers.laptop_controller import laptop_bp
from .Controllers.order_controller import order_bp
from .Controllers.review_controller import review_bp
from .Controllers.user_controller import user_bp

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laptops.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(laptop_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(cart_bp)
    return app
