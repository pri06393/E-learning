from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class UserBase(BaseModel):
    username: str


class UserLogin(UserBase):
    password: str


class StudentRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class InstructorRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class SignupBase(BaseModel):
    username: str
    password: str
    name: str

class StudentSignup(SignupBase):
    pass

class InstructorSignup(SignupBase):
    is_admin: bool

class CreateAttempt(BaseModel):
    quiz_id: int 
    student_id: int
