from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter, UploadFile, Form
from fastapi.params import File
from sqlmodel import Field, Session, SQLModel, create_engine, select
from src.database import create_db_and_tables, engine, SessionLocal, get_db
from pydantic import BaseModel
from fastapi.responses import FileResponse
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

@router.post("/upload", response_model=schemas.ContentRead)
async def upload_content(
    title: str = Form(...),               
    description: str | None = Form(None), 
    file: UploadFile = File(...),         
    db: Session = Depends(get_db),
    current_user: Password = Depends(get_current_user)
):
    content_data = schemas.ContentCreate(
        title=title,
        description=description
    )
    return await service.create_content(content_data, file, db)


@router.get("/{content_id}", response_model=schemas.ContentRead)
async def get_content(
    content_id: int,
    current_user: Password = Depends(get_current_user),  
    db: Session = Depends(get_db),
):
    return await service.get_content(content_id, db)

@router.get("/{content_id}/download")
async def download_content(
    content_id: int,
    current_user: Password = Depends(get_current_user),  
    db: Session = Depends(get_db),
):
    content = await service.get_content(content_id, db)
    return FileResponse(content.file_url, filename=content.file_url.split("/")[-1])
