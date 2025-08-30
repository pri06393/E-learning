from sqlalchemy.orm import Session
from learning import models, schemas,  database
from fastapi import Depends
def create_course(course: schemas.Courses, db: Session= Depends(database.get_db)):
    new_course = models.Courses(
        I_id=course.I_id,
        Course_name=course.Course_name,
        Course_duration=course.Course_duration
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course
def list_courses(db: Session):
    return db.query(models.Courses).all()
def get_course(course_id: int, db: Session):
    return db.query(models.Courses).filter(models.Courses.C_id == course_id).first()