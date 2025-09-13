from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    name: str
    instructor_id: int

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    instructor_id: Optional[int] = None

class CourseRead(BaseModel):
    id: int
    name: str
    instructor_id: Optional[int] = None

    class Config:
        orm_mode = True

class ModuleCreate(BaseModel):
    name: str
    course_id: int

class ModuleUpdate(BaseModel):
    name: Optional[str] = None


class ModuleRead(BaseModel):
    id: int
    name: str
    course_id: int

    class Config:
        orm_mode = True