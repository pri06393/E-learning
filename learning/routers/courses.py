from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from learning import schemas, database, auth, models
from learning.repository import courses as course_repo
from learning.auth import oauth2_scheme
router = APIRouter(prefix="/courses", tags=["Courses"])
@router.post("/", response_model=schemas.CoursesRead)
def create_course( course: schemas.Courses, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.role_required("Instructor"))):
    return course_repo.create_course(course, db)

@router.get("/", response_model=list[schemas.CoursesRead])
def list_courses(db: Session = Depends(database.get_db)):
    return course_repo.list_courses(db)

@router.get("/{course_id}", response_model=schemas.CoursesRead)
def get_course(course_id: int, db: Session = Depends(database.get_db)):
    return course_repo.get_course(course_id, db)