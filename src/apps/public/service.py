

from src.apps.course.model import Course
from sqlmodel import Session


def read_courses(db: Session):
    query = db.query(Course)
    courses = query.all()

    return courses