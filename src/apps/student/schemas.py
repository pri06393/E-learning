from pydantic import BaseModel


class ShowStudent(BaseModel):
    id: int
    name: str
    age: int | None = None

    class Config:
        orm_mode = True

class EnrollmentCreate(BaseModel):
    course_id: int

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None  