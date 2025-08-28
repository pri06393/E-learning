from sqlalchemy.orm import Session
from learning import models, schemas, database
from fastapi import Depends
def create_enrollment(enroll: schemas.EnrollmentCreate, db: Session= Depends(database.get_db)):
    new_enrollment = models.Enrollment(C_id=enroll.C_id, S_id=enroll.S_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment
def list_enrollments(db: Session):
    return db.query(models.Enrollment).all()
def get_enrollment(enroll_id: int, db: Session):
    return db.query(models.Enrollment).filter(models.Enrollment.Enrollment_id == enroll_id).first()