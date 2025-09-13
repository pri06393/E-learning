from sqlalchemy.orm import Session
from . import model, schemas
from src.database import create_db_and_tables, engine, SessionLocal, get_db
from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter, File, UploadFile, Form 

from src.apps.user.model import Password
from src.apps.course.model import Course
from src.core.dependencies import require_instructor
from src.apps.instructor.model import Instructor

def create_instructor(db: Session, instructor: schemas.InstructorCreate):
    instructor_obj = model.Instructor(**instructor.dict())
    with Session(engine) as session:
        session.add(instructor_obj)
        session.commit()
        session.refresh(instructor_obj)
        return instructor_obj
    
def read_my_courses(current_user: Password ,db: Session):
    # if current_user.instructor_id == None:
    #     raise HTTPException(status_code=403, detail="only instructors allowed")
    
    query = db.query(Course).filter(Course.instructor_id == current_user.instructor_id)
    courses = query.all()

    if not courses:
        return "No courses found"

    return courses 

def update_instructor(
    instructor_id: int,
    updated_data: dict,
    current_user: Password,
    db: Session 
):

    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    if instructor.id != current_user.instructor_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this instructor")

    for key, value in updated_data.items():
        setattr(instructor, key, value)

    db.commit()
    db.refresh(instructor)
    return {"message": "Instructor updated successfully", "instructor": instructor}

# @router.delete("/{instructor_id}")
def delete_instructor(
    instructor_id: int,
    current_user,
    db: Session
):
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    user = db.query(Password).filter(Password.instructor_id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    if instructor.id != current_user.instructor_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this instructor")
    
    if user:
        db.delete(user)
        db.commit()
        db.refresh(user)

    db.delete(instructor)
    db.commit()
    db.refresh(instructor)  
    return {"message": "Instructor deleted successfully"}