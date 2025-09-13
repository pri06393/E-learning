from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel
from sqlalchemy import LargeBinary, Column

from src.apps.instructor.model import Instructor
from src.apps.student.model import Student
from src.apps.enrollment.model import StudentCourseLink
from src.apps.quiz.model import Quiz


class Course(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    instructor_id: int | None = Field(foreign_key="instructor.id")
    instructor: Instructor | None = Relationship(back_populates="courses")
    
    students: list[Student] = Relationship(back_populates="courses", link_model=StudentCourseLink)
    modules: list["Module"] = Relationship(back_populates="course")

class Module(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    course_id: int | None = Field(foreign_key="course.id")
    course: Course | None = Relationship(back_populates="modules")

    contents: list["Content"] = Relationship(back_populates="module")

    quizes: list["Quiz"] = Relationship(back_populates="module")

# class Content(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     binary_data: bytes = Field(sa_column=Column(LargeBinary))

#     module_id: int | None = Field(foreign_key="module.id")
#     module: Module | None = Relationship(back_populates="contents")

