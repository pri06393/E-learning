from fastapi import APIRouter, Depends
from learning import schemas, database, models
from typing import List
from sqlalchemy.orm import Session
router = APIRouter()


@router.get("/courses_list",response_model=schemas.CoursesRead)
def course_list(db: Session = Depends(database.get_db)):
    course_list = db.query(models.Courses).all()
    return course_list