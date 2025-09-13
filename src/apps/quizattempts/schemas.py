from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, create_engine

class ResultBase(SQLModel):
    answer_set: str
    # student_quiz_id: int

class ResultCreate(ResultBase):
    pass