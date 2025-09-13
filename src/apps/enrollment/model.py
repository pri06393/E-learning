from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel
from sqlalchemy import LargeBinary, Column

class StudentCourseLink(SQLModel, table=True, ondelete="CASCADE"):
    course_id: int | None = Field(foreign_key="course.id", primary_key=True)
    student_id: int | None = Field(foreign_key="student.id", primary_key=True)