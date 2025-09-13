from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select
from src.database import create_db_and_tables, engine, SessionLocal, get_db
from pydantic import BaseModel
# from src.models import Student, Instructor, Course, StudentCourseLink, Module, ContentType, Content, Quiz, StudentQuizLink, Question, Result, ResultCreate, Password
from src.validation import check_question, check_answer, check_answer_set
import json
from typing import Annotated
import requests

from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from src.schemas import Token, StudentSignup, InstructorSignup
# from src.auth import verify_password, create_access_token, decode_access_token, hash_password, get_current_user
from typing import Optional
from . import schemas, service
from src.apps.user.model import Password
from src.apps.instructor.model import Instructor
from src.apps.course.schemas import CourseRead
from src.core.dependencies import require_instructor    


router = APIRouter(prefix="/instructors", tags=["Instructors"])

@router.post("/", response_model=schemas.InstructorRead)
def create_instructor(course: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return service.create_instructor(db, course)

@router.get("/my-courses", response_model=list[CourseRead])
def read_my_courses(current_user: Password = Depends(require_instructor),db: Session = Depends(get_db)):
    return service.read_my_courses(current_user, db)

@router.put("/{instructor_id}", response_model=schemas.InstructorResponse)
def update_instructor(
    instructor_id: int,
    updated_data: schemas.InstructorUpdate,
    current_user: Password = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    return service.update_instructor(instructor_id, updated_data.dict(exclude_unset=True), current_user, db)      

@router.delete("/{instructor_id}", response_model=None)
def delete_instructor(
    instructor_id: int,
    current_user: Password = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    return service.delete_instructor(instructor_id, current_user, db)
