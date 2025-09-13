from sqlalchemy.orm import Session
from . import model, schemas
from src.database import create_db_and_tables, engine, SessionLocal, get_db
from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter, File, UploadFile, Form 
from src.apps.user.model import Password

def create_course(db: Session, course: schemas.CourseCreate):
    course_obj = model.Course(**course.dict())
    with Session(engine) as session:
        session.add(course_obj)
        session.commit()
        session.refresh(course_obj)
        return course_obj

def read_courses(db: Session):
    query = db.query(model.Course)
    courses = query.all()

    return courses
    
def update_course(course_id: int, new_data: schemas.CourseUpdate, db: Session):
    # if current_user.instructor == None:
    #     raise HTTPException(status_code=403, detail="only instructor allowed")
    
    db_course = db.get(model.Course, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db_course.name = new_data.name

    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(course_id: int, db: Session):
    db_course = db.get(model.Course, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(db_course)
    db.commit()
    return {"detail": "Course deleted successfully"}


def create_module(module: schemas.ModuleCreate, current_user: Password, db: Session):
    module = model.Module(**module.dict())
    if current_user.instructor_id == None:
        raise HTTPException(status_code=403, detail="only instructors allowed")
    
    course = db.get(model.Course, module.course_id)
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.instructor_id != current_user.instructor_id:
        raise HTTPException(status_code=403, detail="Not your course")
        
    with Session(engine) as session:
        session.add(module)
        session.commit()
        session.refresh(module)
        return module

def update_module(
    module_id: int,
    updated_data: schemas.ModuleUpdate,
    current_user: Password,
    db: Session
):
    updated_data = updated_data.dict(exclude_unset=True)
    module = db.query(model.Module).filter(model.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    course = db.get(model.Course, module.course_id)
    if not course or course.instructor_id != current_user.instructor_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this module")

    for key, value in updated_data.items():
        setattr(module, key, value)

    db.commit()
    db.refresh(module)
    return module

def delete_module(
    module_id: int,
    current_user: Password,
    db: Session
):
    module = db.query(model.Module).filter(model.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    course = db.get(model.Course, module.course_id)
    if not course or course.instructor_id != current_user.instructor_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this module")

    db.delete(module)
    db.commit()
    return {"message": "Module deleted successfully"}
