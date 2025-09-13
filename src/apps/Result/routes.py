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
from . import schemas, model, service
from src.database import create_db_and_tables, engine, SessionLocal, get_db
from src.validation import check_question, check_answer, check_answer_set
from src.apps.user.model import Password
from src.core.dependencies import require_instructor, require_student

router = APIRouter(prefix="/results", tags=["results"], dependencies=[Depends(require_student)])

@router.get("/me")
def read_my_result(current_user: Password = Depends(require_student), db: Session = Depends(get_db)):
    return service.read_my_result(current_user, db)