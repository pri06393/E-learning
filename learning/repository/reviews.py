from sqlalchemy.orm import Session
from learning import models, schemas, database
from fastapi import Depends
def create_review(review: schemas.ReviewCreate, db: Session= Depends(database.get_db)):
    new_review = models.Review(
        C_id=review.C_id,
        S_id=review.S_id,
        content=review.content
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
def list_reviews(db: Session):
    return db.query(models.Review).all()
def get_review(review_id: int, db: Session):
    return db.query(models.Review).filter(models.Review.R_id == review_id).first()