from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from typing import Literal
import enum
from sqlalchemy.orm import relationship
class Instructor(Base):
    __tablename__ = "Instructors"
    I_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    I_name = Column(String)
    # I_lastname = models.CharField(max_length=20)
    I_age = Column(Integer)
    creator = relationship("Courses", back_populates="course_creator")
    
class Courses(Base):
    __tablename__ = "Courses"
    C_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    I_id = Column(Integer, ForeignKey("Instructors.I_id"))
    Course_name = Column(String, unique=True, index=True)
    Course_name = Column(String, unique=True, index=True)
    Course_duration = Column(Integer, index=True)
    course_creator = relationship("Instructor", back_populates = "creator")
    course_module = relationship("Modules", back_populates="module_course")
    course_enrollment = relationship("Enrollment", back_populates="enrollment_course")
    
class Modules(Base):
    __tablename__ = "Modules"
    M_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    C_id = Column(Integer, ForeignKey("Courses.C_id"))
    Module_name = Column(String, unique=True, index=True)
    learning_content = Column(String,index = True)
    module_course = relationship("Courses", back_populates="course_module")
# class LearningContent(models.Model):
#     __tablename__ = "Learning Content"
#     L_id = models.AutoField(primary_key=True)
    
class Enrollment(Base):
    __tablename__ = "Enrollment"
    E_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    C_id = Column(Integer, ForeignKey("Courses.C_id"))
    S_id = Column(Integer, ForeignKey("Students.S_id"))
    enrollment_course  = relationship("Courses", back_populates="course_enrollment")
    enrollment_student = relationship("Students", back_populates="student_enrollment")
    enrollment_review = relationship("Reviews", back_populates="review_enrollment")
    
class Reviews(Base):
    __tablename__ = "Reviews"
    R_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Rating = Column(Integer, unique=True, index=True)  #apply restriction to limit the value upto 5 (later)
    review = Column(String, unique=True, index=True)
    E_id = Column(Integer, ForeignKey("Enrollment.E_id"))
    review_enrollment = relationship("Enrollment",back_populates="enrollment_review")
    
class Students(Base):
    __tablename__ = "Students"
    S_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    S_name = Column(String)
    S_age = Column(Integer)
    student_enrollment = relationship("Enrollment", back_populates="enrollment_student")
class Results(Base):
    __tablename__ = "Results"
    Rs_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Q_id  = Column(Integer, ForeignKey("Quiz.Q_id"))
    Qs_id = Column(Integer, ForeignKey("Question.Qs_id"))
    marks = Column(Integer, unique=True, index=True)
    result_quiz = relationship("Quiz", back_populates="quiz_result")
    result_question = relationship("Question", back_populates="question_result")
class Quiz(Base):
    __tablename__ = "Quiz"
    Q_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Quiz_name = Column(String, unique = True, index = True)
    M_id = Column(Integer, ForeignKey("Modules.M_id"))
    quiz_result = relationship("Results", back_populates="result_quiz")

class Question(Base):
    __tablename__ = "Question"
    Qs_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Qs = Column(String, unique = True, index = True)
    Qs_points = Column(Integer, unique = True, index = True)
    question_result = relationship("Results", back_populates="result_question")
    
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
    



 