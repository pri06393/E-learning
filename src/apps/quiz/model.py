from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel
from sqlalchemy import LargeBinary, Column

from src.apps.instructor.model import Instructor
# from src.apps.student.model import Student
from src.apps.enrollment.model import StudentCourseLink
# from src.apps.course.model import Module
from src.apps.Result.model import QuizResult
from src.apps.quizattempts.model import StudentQuizLink


class Quiz(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    module_id: int | None = Field(foreign_key="module.id")
    module: Optional["Module"] = Relationship(back_populates="quizes")

    questions: list["Question"] = Relationship(back_populates="quiz")
    students: list["Student"] = Relationship(back_populates="quizes", link_model=StudentQuizLink)

class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_content: str
    question_answers: str

    quiz_id: int | None = Field(foreign_key="quiz.id")
    quiz: Quiz | None = Relationship(back_populates="questions")

