from pydantic import BaseModel
from typing import Optional

class InstructorCreate(BaseModel):
    name: str
    instructor_id: int

class InstructorUpdate(BaseModel):
    name: Optional[str] = None
    instructor_id: Optional[str] = None

class InstructorRead(BaseModel):
    id: int
    name: str
    instructor_id: int

    class Config:
        orm_mode = True