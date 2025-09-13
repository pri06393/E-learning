from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel
from sqlalchemy import LargeBinary, Column


# from src.apps.course.model import Module
from src.apps.Result.model import QuizResult

class StudentQuizLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(foreign_key="quiz.id")
    student_id: int | None = Field(foreign_key="student.id")

    results: list["QuizResult"] = Relationship(back_populates="student_quiz")



