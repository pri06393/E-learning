from fastapi import FastAPI, Depends, Request, HTTPException, status
import psycopg2
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from learning import schemas, models,database, routers
from passlib.context import CryptContext
app = FastAPI()
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, Response
from typing import List
from learning.routers import learn, user,courses, enrollment, instructor,learn, quiz, reviews, student, user
from fastapi.security import OAuth2PasswordBearer
from learning import auth

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

models.Base.metadata.create_all(engine)

app.include_router(learn.router)

app.include_router(user.router)
app.include_router(instructor.router)
app.include_router(student.router)
app.include_router(courses.router)
app.include_router(quiz.router)
app.include_router(enrollment.router)
app.include_router(reviews.router)
# app.include_router(auth.router)
app.include_router(user.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")    
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
# @app.post('/user')
# def create_user(user:schemas.UserCreate,db:Session = Depends(database.get_db)):
#     hashedPassword = pwd_cxt.hash(user.password)
#     new_user = models.User(name = user.name, email = user.email, password = hashedPassword, role = user.role)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get('/user/{U_id}',response_model= schemas.User)
# def user_id(U_id:int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.U_id ==U_id).first()
#     if not user:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = F"User with the id {U_id} is not found")
#     return user

# @app.post('/instructor/create')   #give access to instructor #registration
# def Instructor_create(instructor:schemas.InstructorCreate,db:Session = Depends(database.get_db)):
#     new_Instructor = models.Instructor(I_name = instructor.I_name, I_age = instructor.I_age)
#     db.add(new_Instructor)
#     db.commit()
#     db.refresh(new_Instructor)
#     return new_Instructor


# @app.get("/instructor_list")
# def Instructor_list(db: Session = Depends(get_db)):
#     instructors_list = db.query(models.Instructor).all()
#     return instructors_list

# @app.get("/instructor/{I_id}" ,response_model= schemas.InstructorRead)
# def Instructor_byid(I_id: int,db: Session = Depends(get_db)):
#     instructor = db.query(models.Instructor).filter(models.Instructor.I_id == I_id).first()
#     return instructor


# @app.post('/Student/create')
# #registration
# def Student_create(student:schemas.StudentCreate,db:Session = Depends(database.get_db)):
#     new_Student = models.Students(S_name = student.S_name, S_age = student.S_age)
#     db.add(new_Student)
#     db.commit()
#     db.refresh(new_Student)
#     return new_Student

# @app.get("/student_list")
# def Student_list(db: Session = Depends(get_db)):
#     students_list = db.query(models.Students).all()
#     return students_list


# @app.get("/student/{S_id}")
# def Student_byid(S_id: int,db: Session = Depends(get_db)):
#     student = db.query(models.Students).filter(models.Students.S_id == S_id).first()
#     return student

# #Create results. Here results from test by the student will be stored
# @app.post('instructor/quiz/results')
# def quiz_create(quiz:schemas.Quiz,db:Session = Depends(database.get_db)):
#     new_quiz = models.Results(Quiz_name = quiz.Quiz_name, Rs_id = quiz.Rs_id, M_id = quiz.M_id)
#     db.add(new_quiz) 
#     db.commit()
#     db.refresh(new_quiz)
#     return new_quiz

# @app.get("/instructor_list")
# def Instructor_list(db: Session = Depends(get_db)):
#     instructor_list = db.query(models.Instructor).all()
#     return instructor_list

# @app.get("/instructor/{I_id}")
# def Instructor_byid(I_id: int,db: Session = Depends(get_db)):
#     instructor = db.query(models.Instructor).filter(models.Instructor.I_id == I_id).first()
#     return instructor

# @app.post('/instructor/question/create')
# def question_create(question:schemas.Question, db:Session = Depends(database.get_db)):
#     new_question = models.Question(Qs = question.Qs, Qs_points = question.Qs_points)
#     db.add(new_question)
#     db.commit()
#     db.refresh(new_question)
#     return new_question

# @app.get("/question_list")
# def Question_list(db: Session = Depends(get_db)):
#     Question_list = db.query(models.Question).all()
#     return Question_list


# #get courses by instructor id

# #RESULTS CREATION

# @app.post('/Instructor/Courses/create')   #give access to instructor
# def Course_create(courses:schemas.Courses,db:Session = Depends(database.get_db)):
#     new_Courses = models.Courses(I_id = courses.I_id, Course_name = courses.Course_name, Course_duration = courses.Course_duration )
#     db.add(new_Courses)
#     db.commit()
#     db.refresh(new_Courses)
#     return new_Courses

# # @app.get("/courses_list",response_model=schemas.CoursesRead)
# # def course_list(db: Session = Depends(get_db)):
# #     course_list = db.query(models.Courses).all()
# #     return course_list

# @app.post('/Instructor/enroll')
# def Enrollment_create(enrollment:schemas.Enrollment,db:Session = Depends(database.get_db)):
#     new_Enrollment = models.Enrollment(C_id = enrollment.C_id, S_id = enrollment.S_id)
#     db.add(new_Enrollment)
#     db.commit()
#     db.refresh(new_Enrollment)
#     return new_Enrollment








