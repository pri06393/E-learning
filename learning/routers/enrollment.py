from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from learning import schemas, database
from learning.repository import enrollment as enrollment_repo
router = APIRouter(prefix="/enrollments", tags=["Enrollments"])
@router.post("/", response_model=schemas.EnrollmentRead)
def create_enrollment(enroll: schemas.EnrollmentCreate, db: Session = Depends(database.get_db)):
    return enrollment_repo.create_enrollment(enroll, db)
@router.get("/", response_model=list[schemas.EnrollmentRead])
def list_enrollments(db: Session = Depends(database.get_db)):
    return enrollment_repo.list_enrollments(db)
@router.get("/{enroll_id}", response_model=schemas.EnrollmentRead)
def get_enrollment(enroll_id: int, db: Session = Depends(database.get_db)):
    return enrollment_repo.get_enrollment(enroll_id, db)