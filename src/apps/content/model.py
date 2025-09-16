from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel
from sqlalchemy import LargeBinary, Column
from datetime import datetime
from src.apps.instructor.model import Instructor
from src.apps.student.model import Student
from src.apps.enrollment.model import StudentCourseLink




class Content(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable = False)
    description: Optional[str] = None
    file_url: str = Field(nullable=False)
    file_type: str = Field(nullable=False)
    uploaded_at: datetime =  Field(default_factory=datetime.utcnow)
    module_id: int | None = Field(foreign_key="module.id")
    module: Optional["Module"] = Relationship(back_populates="contents")

