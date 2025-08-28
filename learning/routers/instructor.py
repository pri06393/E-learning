from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from learning import schemas, database
from learning.repository import instructor as instructor_repo
router = APIRouter(prefix="/instructors", tags=["Instructors"])
@router.post("/", response_model=schemas.InstructorRead)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(database.get_db)):
    return instructor_repo.create_instructor(db, instructor)
@router.get("/", response_model=list[schemas.InstructorRead])
def list_instructors(db: Session = Depends(database.get_db)):
    return instructor_repo.list_instructors(db)
@router.get("/{I_id}", response_model=schemas.InstructorRead)
def get_instructor(I_id: int, db: Session = Depends(database.get_db)):
    instructor = instructor_repo.get_instructor(I_id, db)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor