from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select

from pydantic import BaseModel

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

from src.apps.quizattempts.model import StudentQuizLink
from . import schemas, model
from src.database import create_db_and_tables, engine, SessionLocal, get_db
from src.validation import check_question, check_answer, check_answer_set
from src.apps.user.model import Password


# @router.get("/me")
def read_my_result(current_user: Password, db: Session):
    
    query = db.query(StudentQuizLink.id).filter(StudentQuizLink.student_id == current_user.student_id)
    student_quiz_id = db.scalars(query).all()

    query = db.query(model.QuizResult).filter(model.QuizResult.student_quiz_id.in_(student_quiz_id))
    results = query.all()

    return ("results: ",results)
