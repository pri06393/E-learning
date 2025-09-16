from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContentBase(BaseModel):
    title:str
    description: Optional[str]= None
    
class ContentCreate(ContentBase):
    pass

class ContentRead(ContentBase):
    id: int
    file_url: str
    file_type: str
    uploaded_at: datetime
    
    class Config:
        orm_mode = True