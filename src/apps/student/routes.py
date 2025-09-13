from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select
from src.apps.Result.schemas import ResultCreate
from src.apps.course.schemas import CourseRead
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
from src.auth import verify_password, create_access_token, decode_access_token, hash_password, get_current_user
from typing import Optional, List
from . import schemas, service

from src.apps.user.model import Password
from src.core.dependencies import require_student

router = APIRouter(prefix="/students", tags=["students"], dependencies=[Depends(require_student)])

@router.get("/me", response_model=schemas.ShowStudent)
def read_student_me(current_user: Password = Depends(get_current_user)):
    return service.read_student_me(current_user)

@router.post("/enroll/", response_model=schemas.EnrollmentCreate)
def create_enrollment(enrollment: schemas.EnrollmentCreate, current_user: Password = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.create_enrollment(enrollment, current_user, db)

@router.get("/my_courses/", response_model=List[CourseRead])
def read_my_courses(current_user: Password = Depends(get_current_user),db: Session = Depends(get_db)):
    return service.read_my_courses(current_user, db)

@router.put("/update_me", response_model=schemas.StudentUpdate)
def update_student_me(new_data: schemas.StudentUpdate, current_user: Password = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.update_student_me(new_data, current_user, db)

@router.delete("/delete_me", response_model=None)
def delete_student_me(current_user: Password = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.delete_student_me(current_user, db)

@router.delete("/unenroll/{course_id}", response_model=None)
def unenroll_course(course_id: int, current_user: Password = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.unenroll_course(course_id, current_user, db)

@router.post("/submit/{quiz_id}")
def create_result(result: ResultCreate, quiz_id:int, db: Session = Depends(get_db), current_user: Password = Depends(get_current_user)):
    return service.create_result(result, quiz_id, db, current_user)