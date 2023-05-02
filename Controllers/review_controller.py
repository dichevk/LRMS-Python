from flask import Blueprint, jsonify, request, abort
from app import db
from ..Models.laptop_model import Laptop
from ..Models.review_model import Review

review_bp = Blueprint('review', __name__, url_prefix='/review')

# Endpoint for creating a new review for a laptop
@review_bp.route('/<int:laptop_id>', methods=['POST'])
def create_review(laptop_id):
    # Get the laptop for which the review is being created
    laptop = Laptop.query.get(laptop_id)

    if not laptop:
        return jsonify({'message': 'Laptop not found.'}), 404

    # Create the review object
    review = Review(
        laptop=laptop,
        rating=request.json.get('rating'),
        comment=request.json.get('comment')
    )

    # Add the review to the database
    db.session.add(review)
    db.session.commit()

    return jsonify({
        'message': 'Review created successfully.',
        'review': review.to_dict()
    }), 201

# Endpoint for getting all reviews for a laptop
@review_bp.route('/<int:laptop_id>', methods=['GET'])
def get_reviews_for_laptop(laptop_id):
    # Get the laptop for which the reviews are being retrieved
    laptop = Laptop.query.get(laptop_id)

    if not laptop:
        return jsonify({'message': 'Laptop not found.'}), 404

    # Get all reviews for the laptop
    reviews = Review.query.filter_by(laptop_id=laptop_id).all()

    # Return the reviews in JSON format
    return jsonify({
        'reviews': [review.to_dict() for review in reviews]
    }), 200

# Endpoint for updating an existing review
@review_bp.route('/<int:id>', methods=['PUT'])
def update_review(id):
    # Get the review being updated
    review = Review.query.get(id)

    if not review:
        return jsonify({'message': 'Review not found.'}), 404

    # Update the review
    review.rating = request.json.get('rating', review.rating)
    review.comment = request.json.get('comment', review.comment)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({
        'message': 'Review updated successfully.',
        'review': review.to_dict()
    }), 200

# Endpoint for deleting an existing review
@review_bp.route('/<int:id>', methods=['DELETE'])
def delete_review(id):
    # Get the review being deleted
    review = Review.query.get(id)

    if not review:
        return jsonify({'message': 'Review not found.'}), 404

    # Delete the review from the database
    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted successfully.'}), 200
