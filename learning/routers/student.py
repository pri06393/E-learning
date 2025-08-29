from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from learning import schemas, database
from learning.repository import student as student_repo
router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=schemas.StudentRead)
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    return student_repo.create_student(student, db)

@router.get("/", response_model=list[schemas.StudentRead])
def list_students(db: Session = Depends(database.get_db)):
    return student_repo.list_students(db)

@router.get("/{student_id}", response_model=schemas.StudentRead)
def get_student(student_id: int, db: Session = Depends(database.get_db)):
    return student_repo.get_student(student_id, db)