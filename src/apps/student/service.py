from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select

from pydantic import BaseModel

import json
from typing import Annotated
import requests

from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from src.apps.Result.model import QuizResult
from src.apps.quiz.model import Question
from src.apps.quizattempts.model import StudentQuizLink
from src.validation import check_answer_set
from src.apps.Result.schemas import ResultCreate
from src.apps.course.model import Course
from src.apps.enrollment.model import StudentCourseLink
from src.apps.user.model import Password
from . import schemas, model



def read_student_me(current_user: Password):
    return current_user.student

def create_enrollment(enrollment: schemas.EnrollmentCreate, current_user: Password ,db: Session):
 
    enroll = StudentCourseLink(course_id=enrollment.course_id, student_id=current_user.student_id)
    db.add(enroll)
    db.commit()
    db.refresh(enroll)
    return enrollment

def read_my_courses(current_user: Password , db: Session):

    query = db.query(StudentCourseLink.course_id).filter(StudentCourseLink.student_id == current_user.student_id)
    courses_id = db.scalars(query).all()
    
    query = db.query(Course).filter(Course.id.in_(courses_id))
    courses = query.all()

    if not courses:
        return "No courses found"

    return courses

def update_student_me(
    updated_data: dict,
    current_user: Password,
    db: Session 
):
    updated_data = updated_data.dict(exclude_unset=True)
    student = db.query(model.Student).filter(model.Student.id == current_user.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.id != current_user.student_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this student")

    for key, value in updated_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


def delete_student_me(
    current_user,
    db: Session
):
    student = db.query(model.Student).filter(model.Student.id == current_user.student_id).first()
    user = db.query(Password).filter(Password.student_id == current_user.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.id != current_user.student_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this student")
    
    db.delete(user)
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}


def unenroll_course(
    course_id: int,
    current_user,
    db: Session
):

    enrollment = (
        db.query(StudentCourseLink)
        .filter(StudentCourseLink.course_id == course_id)
        .filter(StudentCourseLink.student_id == current_user.student_id)
        .first()
    )

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(enrollment)
    db.commit()
    return {"message": "Enrollment deleted successfully"}

# @router.post("/submit/{quiz_id}")
# def create_result(result: ResultCreate, quiz_id:int, db: Session, current_user: Password):
#     if current_user.student_id == None:
#         raise HTTPException(status_code=403, detail="only students allowed")
    
#     attempt = StudentQuizLink(student_id=current_user.student_id, quiz_id=quiz_id)
#     db.add(attempt)
#     db.commit()
#     db.refresh(attempt)


#     # quiz_id = result.student_quiz_id
#     question_ids = []
#     correct_options = []
    
#     query = db.query(Question).filter(Question.quiz_id == quiz_id)
#     questions = query.all()

#     for question in range(len(questions)):
#         # print(type(questions[question].id))
#         question_ids.append(questions[question].id)
#         correct_options.append(json.loads(questions[question].question_answers))

#     user_result_answer_set = check_answer_set(result.answer_set,question_ids)
#     user_answer_set = json.dumps(user_result_answer_set)
#     # print("user_answer_set:", user_answer_set)
#     user_answer = {int(k): v for k, v in user_result_answer_set.items()}
    
#     correct_answer_set = dict(zip(question_ids, correct_options))
#     # print(questions)
#     # print("correct answer set: ",correct_answer_set)
#     # print("user answer set: ",user_answer_set)

#     marks  = 0

#     for id in question_ids:
#         print(id)
#         print(correct_answer_set[id])
#         if set(correct_answer_set[id]) == set(user_answer[id]):
#             print(f'question {id} is correct')
#             marks = marks + 1
#         else:
#             print(f'question {id} is wrong')

#     result.answer_set = user_result_answer_set
#     db_result = QuizResult(
#         student_quiz_id=attempt.id,
#         answer_set=json.dumps(result.answer_set),
#         marks=marks
#     )
   
#     db.add(db_result)
#     db.commit()
#     db.refresh(db_result)
#     return result

def create_result(result: ResultCreate, quiz_id: int, db: Session, current_user: Password):
    if current_user.student_id is None:
        raise HTTPException(status_code=403, detail="only students allowed")

    # Create student attempt record
    attempt = StudentQuizLink(student_id=current_user.student_id, quiz_id=quiz_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # Fetch all questions for the quiz
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()

    # Build correct answer set {question_id: [options]}
    correct_answer_set = {
        q.id: json.loads(q.question_answers) for q in questions
    }
    question_ids = list(correct_answer_set.keys())

    # ✅ User answers are already coming as dictionary now
    # result.answer_set should look like: {"12": [0,2], "15": [1,2]}
    # Convert keys to int for consistency
    print("answer:", type(result.answer_set))
    try:
        user_answer_set = {int(k): v for k, v in result.answer_set.items()}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid answer_set format")

    marks = 0
    for qid in question_ids:
        correct = set(correct_answer_set[qid])
        user_ans = set(user_answer_set.get(qid, []))  # empty if not answered

        if correct == user_ans:
            marks += 1
            print(f"question {qid} is correct")
        else:
            print(f"question {qid} is wrong")

    # Save quiz result
    db_result = QuizResult(
        student_quiz_id=attempt.id,
        answer_set=json.dumps(user_answer_set),  # Save cleaned dict
        marks=marks
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return {
        "quiz_id": quiz_id,
        "student_id": current_user.student_id,
        "marks": marks,
        "answer_set": user_answer_set
    }