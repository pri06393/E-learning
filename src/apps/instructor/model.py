from sqlmodel import Field, Relationship, SQLModel, create_engine
from pydantic import BaseModel

class Instructor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int | None = None

    courses: list["Course"] = Relationship(back_populates="instructor")
    password: "Password" = Relationship(back_populates="instructor")