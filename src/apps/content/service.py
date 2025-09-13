from fastapi import Depends, FastAPI, Form, HTTPException, Query, APIRouter, UploadFile
from fastapi.params import File
from sqlmodel import Field, Session, SQLModel, create_engine, select
from src.apps.course.model import Course, Module
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
from . import schemas, model


from src.apps.user.model import Password


# @router.post("/create/")
async def create_content(current_user: Password, db: Session, module_id: int = Form(...), file: UploadFile = File(...)):
    module = db.get(Module, module_id)
    course = db.get(Course, module.course_id)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.instructor_id != current_user.instructor_id:
        raise HTTPException(status_code=403, detail="Not your course")

    binary_data_uploaded = await file.read()

    db_content = model.Content(
        module_id=module_id,
        binary_data=binary_data_uploaded
    )

    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    # return db_content
    return "hello"

# @router.put("/{content_id}")
async def update_content(
    content_id: int,
    session: Session,
    module_id: Optional[int] = None,
    file: Optional[UploadFile] = File(None)
):
    content = session.get(model.Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if module_id is not None:
        content.module_id = module_id
    if file is not None:
        content.binary_data = await file.read()

    session.add(content)
    session.commit()
    session.refresh(content)
    return {"message": "Content updated successfully", "id": content.id}

# @router.delete("/{content_id}")
def delete_content(content_id: int, session: Session):
    content = session.get(model.Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    session.delete(content)
    session.commit()
    return {"message": f"Content {content_id} deleted successfully"}