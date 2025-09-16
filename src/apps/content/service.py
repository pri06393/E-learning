import os
import shutil
from datetime import datetime
from sqlmodel import Session
from fastapi import UploadFile
from . import schemas, model  
UPLOAD_DIR = "uploads"
async def create_content(content_data: schemas.ContentCreate, file: UploadFile, db: Session):
   
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
   
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    new_content = model.Content(
        title=content_data.title,
        description=content_data.description,
        file_url=file_path,
        file_type=file.content_type,
        uploaded_at=datetime.utcnow()
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content
async def get_content(content_id: int, db: Session):
    content = db.get(model.Content, content_id)
    if not content:
        raise ValueError(f"Content with id={content_id} not found")
    return content