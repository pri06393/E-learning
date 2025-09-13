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
# from src.schemas import Token, StudentSignup, InstructorSignup
from src.auth import verify_password, create_access_token, decode_access_token, hash_password, get_current_user
from src.apps.user.model import Password
from src.apps.student.model import Student
from src.apps.instructor.model import Instructor


def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    statement = select(Password).where(Password.username == form_data.username)
    creds = db.scalars(statement).first()
    # print("creds: ", type(creds))
    # print("creds: ", creds.id)
    if not creds or not verify_password(form_data.password, creds.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    role = "student" if creds.student_id else "instructor"
    token = create_access_token({"sub": creds.username, "role": role})
    return {"access_token": token, "token_type": "bearer"}