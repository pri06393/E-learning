from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from learning import schemas, database
from learning.repository import reviews as review_repo
router = APIRouter(prefix="/reviews", tags=["Reviews"])
@router.post("/", response_model=schemas.ReviewRead)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(database.get_db)):
    return review_repo.create_review(review, db)
@router.get("/", response_model=list[schemas.ReviewRead])
def list_reviews(db: Session = Depends(database.get_db)):
    return review_repo.list_reviews(db)
@router.get("/{review_id}", response_model=schemas.ReviewRead)
def get_review(review_id: int, db: Session = Depends(database.get_db)):
    return review_repo.get_review(review_id, db)