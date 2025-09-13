from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter, UploadFile
from fastapi.params import File
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

router = APIRouter(prefix="/content", tags=["contents"], dependencies=[Depends(require_instructor)])

# @router.post("/create", response_model=None)
# async def create_content(
#     content: schemas.ContentCreate,
#     file: Optional[UploadFile] = File(None),
#     db: Session = Depends(get_db),
# ):
#     return await service.create_content(content, file, db)