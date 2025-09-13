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
from . import schemas, model
from src.database import create_db_and_tables, engine, SessionLocal, get_db
from src.validation import check_question, check_answer, check_answer_set
from src.apps.user.model import Password


def create_quiz(quiz: schemas.QuizCreate, current_user: Password, db: Session):
    quiz_obj = model.Quiz(**quiz.dict())
    db.add(quiz_obj)
    db.commit()
    db.refresh(quiz_obj)
    return quiz_obj
    

def add_question(quiz_id: int, question: schemas.QuestionCreate,current_user:Password, db: Session):

    # print(question.question_content)
    check_question(question.question_content)
    check_answer(question.question_answers,question.question_content)
    question_obj = model.Question(**question.dict())
    question_obj.quiz_id = quiz_id

    db.add(question_obj)
    db.commit()
    db.refresh(question_obj)
    return question_obj

# @router.get("/{quiz_id}")
def read_question_by_quiz_id(quiz_id: int, db: Session):
    # query = db.query(Question)
    query = db.query(model.Question).filter(model.Question.quiz_id == quiz_id)

    questions = query.all()
    return questions



