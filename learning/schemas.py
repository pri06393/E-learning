from pydantic import BaseModel
from typing import Optional
import enum
#None = None  # Optional field with a default value of None(add using a pipeline)

class Instructor(BaseModel):
    
    I_name : str
    I_age : int
class Courses(BaseModel):
    
    Course_name : str
    I_id : int
    Course_duration : int
class Modules(BaseModel):
    
    C_id : int
    Module_name : str
class Enrollment(BaseModel):
    
    C_id : int
    S_id : int
class Reviews(BaseModel):
    
    Rating : Optional[int] = None
    review : Optional[str] = None
    E_id : int
class Students(BaseModel):
    
    S_name : str
    S_age : int
class Results(BaseModel):
    
    marks : Optional[int] = None
    
class Quiz(BaseModel):
    Quiz_name : str
    Rs_id : int
    M_id : int
    
class Question(BaseModel):
    Qs : str
    Qs_points : int
    
    
    
class InstructorCreate(Instructor):
    pass
class InstructorRead(Instructor):
    I_id:int
    class Config:
        orm_mode:True

class CoursesCreate(Courses):
    pass
class CoursesRead(Courses):
    C_id:int
    class Config:
        orm_mode:True
        
class ModulesCreate(Modules):
    pass
class ModulesRead(Modules):
    M_id:int
    class Config:
        orm_mode:True
        
class EnrollmentCreate(Enrollment):
    pass
class EnrollmentRead(Enrollment):
    E_id:int
    class Config:
        orm_mode:True
        
class ReviewCreate(Reviews):
    pass
class ReviewRead(Reviews):
    R_id:int
    class Config:
        orm_mode:True
        
class StudentCreate(Students):
    pass
class StudentRead(Students):
    S_id:int
    class Config:
        orm_mode:True

class ResultsCreate(Results):
    pass
class ResultsRead(Results):
    S_id:int
    class Config:
        orm_mode:True
        
class QuizRead(Quiz):
    Q_id:int
    class Config:
        orm_mode:True
        
class QuestionRead(Question):
    Qs_id:int
    class Config:
        orm_mode:True
 
class Role(str, enum.Enum):
    Instructor = "Instructor"
    Student = "Student"       

class User(BaseModel):
    name :str
    email:str
    password:str
    role:Role
    
class UserRead(User):
    name:str
    email:str
    class Config:
        orm_mode:True    
