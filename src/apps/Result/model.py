from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel
from sqlalchemy import LargeBinary, Column

from src.apps.instructor.model import Instructor

# from src.apps.quiz.model import StudentQuizLink
# from src.apps.course.model import Module


class QuizResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marks: int
    answer_set: str

    student_quiz_id: int | None = Field(foreign_key="studentquizlink.id")
    student_quiz: Optional["StudentQuizLink"] = Relationship(back_populates="results")
