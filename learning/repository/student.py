from sqlalchemy.orm import Session
from learning import models, schemas, database
from fastapi import Depends
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    new_student = models.Student(
        S_name=student.S_name,
        S_age=student.S_age
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
def list_students(db: Session):
    return db.query(models.Student).all()
def get_student(student_id: int, db: Session):
    return db.query(models.Student).filter(models.Student.S_id == student_id).first()