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


def create_result(result: ResultCreate, quiz_id: int, db: Session, current_user: Password):
    if current_user.student_id is None:
        raise HTTPException(status_code=403, detail="only students allowed")


    attempt = StudentQuizLink(student_id=current_user.student_id, quiz_id=quiz_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)


    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this quiz")


    if isinstance(result.answer_set, str):
        try:
            result.answer_set = json.loads(result.answer_set)
        except Exception:
            raise HTTPException(status_code=400, detail="answer_set must be valid JSON")

    if not isinstance(result.answer_set, dict):
        raise HTTPException(status_code=400, detail="answer_set must be a dictionary")


    user_answer_set = {int(k): v for k, v in result.answer_set.items()}

    total_marks = 0
    detailed_results = {}

    for q in questions:
        qid = q.id

        # print("q: ",json.loads(q.question_content))
        q_c = json.loads(q.question_content)
        # print("c: ", c["options"])
        
        options = q_c["options"]            
        correct_idx = json.loads(q.question_answers)  
        correct_strings = [options[i] for i in correct_idx]  

        user_strings = user_answer_set.get(qid, [])   
        user_strings = [str(ans).strip() for ans in user_strings]  


        correct_set = set(correct_strings)
        user_set = set(user_strings)

        overlap = correct_set.intersection(user_set)
        partial_score = len(overlap) / len(correct_set) if correct_set else 0

        total_marks += partial_score
        detailed_results[qid] = {
            "content": q_c["content"],
            "correct": correct_strings,
            "user": user_strings,
            "score": partial_score
        }

        print(f"Q{qid}: correct={correct_strings}, user={user_strings}, score={partial_score:.2f}")


    db_result = QuizResult(
        student_quiz_id=attempt.id,
        answer_set=json.dumps(user_answer_set),
        marks=round(total_marks)
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return {
        "quiz_id": quiz_id,
        "student_id": current_user.student_id,
        "marks": total_marks,
        "total_questions": len(questions),
        "details": detailed_results
    }
