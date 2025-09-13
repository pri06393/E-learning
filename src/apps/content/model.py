from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel
from sqlalchemy import LargeBinary, Column

from src.apps.instructor.model import Instructor
from src.apps.student.model import Student
from src.apps.enrollment.model import StudentCourseLink
# from src.apps.course.model import Module



class Content(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    binary_data: bytes = Field(sa_column=Column(LargeBinary))

    module_id: int | None = Field(foreign_key="module.id")
    module: Optional["Module"] = Relationship(back_populates="contents")

