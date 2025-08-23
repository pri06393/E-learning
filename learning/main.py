from fastapi import FastAPI, Depends, Request
import psycopg2
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from learning import schemas, models,database
from passlib.context import CryptContext
app = FastAPI()
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, Response


models.Base.metadata.create_all(engine)
# def get_connection():
#     conn = psycopg2.connect(database.SQLALCHEMY_DATABASE_URL)
#     cursor = conn.cursor()
#     return cursor
    # return psycopg2.connect(
    #     database.SQLALCHEMY_DATABASE_URL
    # )
    
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/user')
def create_user(user:schemas.User,db:Session = Depends(database.get_db)):
    hashedPassword = pwd_cxt.hash(user.password)
    new_user = models.User(name = user.name, email = user.email, password = hashedPassword, role = user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/Instructor/create')   #give access to instructor #registration
def Instructor_create(instructor:schemas.InstructorCreate,db:Session = Depends(database.get_db)):
    new_Instructor = models.Instructor(I_name = instructor.I_name, I_age = instructor.I_age)
    db.add(new_Instructor)
    db.commit()
    db.refresh(new_Instructor)
    return new_Instructor

@app.post('Student/create')
#registration
def Student_create(student:schemas.StudentCreate,db:Session = Depends(database.get_db)):
    new_Student = models.Students(S_name = student.S_name, S_age = student.S_age)
    db.add(new_Student)
    db.commit()
    db.refresh(new_Student)
    return new_Student




@app.post('instructor/quiz/results')
def quiz_create(quiz:schemas.Quiz,db:Session = Depends(database.get_db)):
    new_quiz = models.Results(Quiz_name = quiz.Quiz_name, Rs_id = quiz.Rs_id, M_id = quiz.M_id)
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz

@app.post('instructor/question/create')
def question_create(question:schemas.Question, db:Session = Depends(database.get_db)):
    new_question = models.Question(Qs = question.Qs, Qs_points = question.Qs_points)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

#RESULTS CREATION

@app.post('Instructor/Courses/create')   #give access to instructor
def Course_create(courses:schemas.Courses,db:Session = Depends(database.get_db)):
    new_Courses = models.Courses(I_id = courses.I_id, Course_name = courses.Course_name, Course_duration = courses.Course_duration )
    db.add(new_Courses)
    db.commit()
    db.refresh(new_Courses)
    return new_Courses

@app.post('/Instructor/enroll')
def Enrollment_create(enrollment:schemas.Enrollment,db:Session = Depends(database.get_db)):
    new_Enrollment = models.Enrollment(C_id = enrollment.C_id, S_id = enrollment.S_id)
    db.add(new_Enrollment)
    db.commit()
    db.refresh(new_Enrollment)
    return new_Enrollment


@app.get('/user/{id}', response_model=schemas.UserRead) 
def get_user(id:int,db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HttpException(status_code = )
     
     
    
# @app.get("/users")
# def read_users():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT id, name, email FROM users;")
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return {"users": rows}
