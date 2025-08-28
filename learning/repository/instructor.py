from sqlalchemy.orm import Session
from learning import models, schemas, database
from fastapi import Depends
def create_instructor( instructor: schemas.InstructorCreate, db: Session  = Depends(database.get_db)):
    new_instructor = models.Instructor(I_name=instructor.I_name, I_age=instructor.I_age)
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)
    return new_instructor
def list_instructors(db: Session):
    return db.query(models.Instructor).all()
def get_instructor(I_id: int, db: Session):
    return db.query(models.Instructor).filter(models.Instructor.I_id == I_id).first()