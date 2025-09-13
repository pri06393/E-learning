from pydantic import BaseModel
from typing import Optional

class InstructorCreate(BaseModel):
    name: str
    age: int

class InstructorUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

class InstructorRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class InstructorResponse(BaseModel):
    message: str
    instructor: InstructorRead

    class Config:
        orm_mode = True