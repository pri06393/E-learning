from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel

from src.apps.student.model import Student
from src.apps.instructor.model import Instructor

class Password(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    is_admin: bool


    student_id: int | None = Field(foreign_key="student.id")
    student: Student | None = Relationship(back_populates="password")

    instructor_id: int | None = Field(foreign_key="instructor.id")
    instructor: Instructor | None = Relationship(back_populates="password")