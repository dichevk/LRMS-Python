import json
from ..Models.laptop_model import Laptop
from ..Models.review_model import Review
from ..Models.user_model import User

def test_add_review(client, app, db):
    # create a new laptop
    laptop = Laptop(name="Test Laptop", price=1000, specs="Test specs")
    db.session.add(laptop)
    db.session.commit()

    # send a POST request to add a new review for the laptop
    data = {"rating": 4, "comment": "Test comment"}
    response = client.post(f'/laptop/{laptop.id}/review', json=data)

    # check the response
    assert response.status_code == 200
    assert response.json["message"] == "Review added successfully."

    # check if the review is added to the database
    review = Review.query.filter_by(laptop_id=laptop.id).first()
    assert review is not None
    assert review.rating == 4
    assert review.comment == "Test comment"

def test_get_reviews(client, app, db):
    # create a new laptop
    laptop = Laptop(name="Test Laptop", price=1000, specs="Test specs")
    db.session.add(laptop)
    db.session.commit()

    # add two reviews for the laptop
    review1 = Review(rating=4, comment="Test comment 1", laptop_id=laptop.id)
    review2 = Review(rating=5, comment="Test comment 2", laptop_id=laptop.id)
    db.session.add_all([review1, review2])
    db.session.commit()

    # send a GET request to get all the reviews for the laptop
    response = client.get(f'/laptop/{laptop.id}/reviews')

    # check the response
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["rating"] == 4
    assert response.json[0]["comment"] == "Test comment 1"
    assert response.json[1]["rating"] == 5
    assert response.json[1]["comment"] == "Test comment 2"
    
def test_update_review(client, app, db):
    # create a new laptop and add a review for it
    laptop = Laptop(name="Test Laptop", price=1000, specs="Test specs")
    db.session.add(laptop)
    db.session.commit()
    review = Review(rating=4, comment="Test comment", laptop_id=laptop.id)
    db.session.add(review)
    db.session.commit()

    # send a PUT request to update the review
    data = {"rating": 5, "comment": "Updated comment"}
    response = client.put(f'/laptop/{laptop.id}/review/{review.id}', json=data)

    # check the response
    assert response.status_code == 200
    assert response.json["message"] == "Review updated successfully."

    # check if the review is updated in the database
    updated_review = Review.query.filter_by(id=review.id).first()
    assert updated_review.rating == 5
    assert updated_review.comment == "Updated comment"

def test_delete_review(client, app, db):
    # create a new laptop and add a review for it
    laptop = Laptop(name="Test Laptop", price=1000, specs="Test specs")
    db.session.add(laptop)
    db.session.commit()
    review = Review(rating=4, comment="Test comment", laptop_id=laptop.id)
    db.session.add(review)
    db.session.commit()

    # send a DELETE request to delete the review
    response = client.delete(f'/laptop/{laptop.id}/review/{review.id}')

    # check the response
    assert response.status_code == 204
    assert Review.query.filter_by(id=review.id).first() is None
