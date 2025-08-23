from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from typing import Literal
import enum
class Instructor(Base):
    __tablename__ = "Instructors"
    I_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    I_name = Column(String, index=True)
    # I_lastname = models.CharField(max_length=20)
    I_age = Column(Integer, index=True)
    
class Courses(Base):
    __tablename__ = "Courses"
    C_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    I_id = Column(Integer, ForeignKey("Instructors.I_id"))
    Course_name = Column(String, unique=True, index=True)
    # Course_name = Column(String, unique=True, index=True)
    Course_duration = Column(Integer, index=True)
    
class Modules(Base):
    __tablename__ = "Modules"
    M_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    C_id = Column(Integer, ForeignKey("Courses.C_id"))
    Module_name = Column(String, unique=True, index=True)
    # learning_content = 
    
# class LearningContent(models.Model):
#     __tablename__ = "Learning Content"
#     L_id = models.AutoField(primary_key=True)
    
class Enrollment(Base):
    __tablename__ = "Enrollment"
    E_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    C_id = Column(Integer, ForeignKey("Courses.C_id"))
    S_id = Column(Integer, ForeignKey("Students.I_id"))
    
    
class Reviews(Base):
    __tablename__ = "Reviews"
    R_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Rating = Column(Integer, unique=True, index=True)  #apply restriction to limit the value upto 5 (later)
    review = Column(String, unique=True, index=True)
    E_id = Column(Integer, ForeignKey("Enrollment.E_id"))
    
class Students(Base):
    __tablename__ = "Students"
    S_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    S_name = Column(String, unique=True, index=True)
    S_age = Column(Integer, unique=True, index=True)
    
class Results(Base):
    __tablename__ = "Results"
    Rs_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Q_id  = Column(Integer, ForeignKey("Quiz.Q_id"))
    marks = Column(Integer, unique=True, index=True)
    
class Quiz(Base):
    __tablename__ = "Quiz"
    Q_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Quiz_name = Column(String, unique = True, index = True)
    Rs_id  = Column(Integer, ForeignKey("Results.Rs_id"))
    M_id = Column(Integer, ForeignKey("Modules.M_id"))

class Question(Base):
    __tablename__ = "Question"
    Qs_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Qs = Column(String, unique = True, index = True)
    Qs_points = Column(Integer, unique = True, index = True)
    
class Role(str, enum.Enum):
    Instructor = "Instructor"
    Student = "Student"
    
class User(Base):
    __tablename__ = "Users"
    U_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Enum(Role), nullable = False, default=Role.Student)
    



 