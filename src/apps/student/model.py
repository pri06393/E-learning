from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel
from src.apps.enrollment.model import StudentCourseLink
from src.apps.quizattempts.model import StudentQuizLink

class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    name: str
    age: int | None = None

    courses: list["Course"] = Relationship(back_populates="students",link_model=StudentCourseLink)
    quizes: list["Quiz"] = Relationship(back_populates="students", link_model=StudentQuizLink)
    password: "Password" = Relationship(back_populates="student")