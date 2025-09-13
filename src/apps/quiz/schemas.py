from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, create_engine


class QuestionCreate(BaseModel):
    question_content: str
    question_answers: str
    quiz_id: int

class QuizCreate(BaseModel):
    name: str
    module_id: int  

class QuizRead(BaseModel):
    id: int
    name: str
    module_id: int

class QuestionRead(BaseModel):
    id: int
    question_content: str
    question_answers: str
    quiz_id: int
