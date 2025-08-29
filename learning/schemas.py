from pydantic import BaseModel, EmailStr
from typing import Optional, List
import enum
#None = None  # Optional field with a default value of None(add using a pipeline)

class Instructor(BaseModel):
    I_name : str
    I_age : int
    # I_name : str
    # I_age : int
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
# class Results(BaseModel):
    
#     marks : Optional[int] = None
    
class Quiz(BaseModel):
    Quiz_name : str
    # Rs_id : int
    # M_id : int
    
class Question(BaseModel):
    Qs : str
    Qs_points : int
    
    
class CoursesRead(Courses):
    C_id:int
    class Config:
        orm_mode:True   
class InstructorCreate(BaseModel):
    I_name : str
    I_age : int
class InstructorRead(Instructor):
    I_id:int
    creator:List[Courses]   #remove the I_id field later
    class Config:
        orm_mode:True

class CoursesCreate(Courses):
    pass

        
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

# class ResultsCreate(Results):
#     pass
# class ResultsRead(Results):
#     S_id:int
#     class Config:
#         orm_mode:True


        

        

class QuestionCreate(BaseModel):
    # Q_id:int
    Qs: str
    option_a:str
    option_b:str
    option_c:str
    option_d:str
    correct_option : str

class QuestionRead(BaseModel):
    Q_id:int
    Qs_id : int
    Qs: str
    option_a:str
    option_b:str
    option_c:str
    option_d:str
    class Config:
        orm_mode:True 

class QuizCreate(BaseModel):
    Quiz_name: str
    Questions : List[QuestionCreate]   
    
class StudentAnswer(BaseModel):
    Qs_id:int
    Q_id:int
    selected_option:str
    

    
class QuizRead(BaseModel):
    Q_id:int
    Quiz_name: str
    quiz_question : List[QuestionRead]    #this is fetched while appearing for a test
    class Config:
        orm_mode:True  
# class QuestionRead(Question):
#     Qs_id:int
#     class Config:
#         orm_mode:True
 
class Role(str, enum.Enum):
    Instructor = "Instructor"
    Student = "Student"       


    
class User(BaseModel):
    name:str
    email:str  
    class Config:
        orm_mode:True   
        
class UserCreate(User):
    name :str
    email:str
    password:str
    role:Role 

class UserListRead(User):
    U_id:int
    name:str
    email:str
    class Config:
        orm_mode:True 
        
class QuizResult(BaseModel):
    score:int
    total:int
    
class Role(str, enum.Enum):
    Instructor = "Instructor"
    Student = "Student"
class UserBase(BaseModel):
    name: str
    email: EmailStr
class UserCreate(UserBase):
    password: str
    role: Role
class UserRead(UserBase):
    U_id: int
    role: Role
    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserLogin(BaseModel):
    email: EmailStr
    passwod:str



