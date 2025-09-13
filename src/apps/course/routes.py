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
from src.auth import verify_password, create_access_token, decode_access_token, hash_password, get_current_user
from typing import Optional, List
from . import schemas, service

from src.apps.user.model import Password
from src.core.dependencies import require_instructor

router = APIRouter(prefix="/courses", tags=["Courses"], dependencies=[Depends(require_instructor)])

@router.post("/create", response_model=schemas.CourseRead)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return service.create_course(db, course)

@router.put("/{course_id}", response_model=schemas.CourseRead)
def update_course(course_id: int, new_data: schemas.CourseUpdate, db: Session = Depends(get_db)):
    return service.update_course(course_id, new_data, db)

@router.delete("/{course_id}", response_model=None)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    return service.delete_course(course_id, db)

@router.post("/modules/create", response_model=schemas.ModuleRead)
def create_module(module: schemas.ModuleCreate, current_user: Password = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.create_module(module, current_user, db)

@router.put("/modules/{module_id}", response_model=schemas.ModuleRead)
def update_module(module_id: int, new_data: schemas.ModuleUpdate, current_user: Password = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.update_module(module_id, new_data, current_user, db)

@router.delete("/modules/{module_id}", response_model=None)
def delete_module(module_id: int, current_user: Password = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.delete_module(module_id, current_user, db)