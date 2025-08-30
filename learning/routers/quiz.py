from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from learning import schemas, database
from learning.repository import quiz as quiz_repo
from typing import List
router = APIRouter(prefix="/quizzes", tags=["Quizzes"])
@router.post("/", response_model=schemas.QuizRead)
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(database.get_db)):
    return quiz_repo.Quiz_create(quiz, db)

@router.get("/")
def list_quizzes(db: Session = Depends(database.get_db)):
    return quiz_repo.Quiz_read_list(db)


@router.get("/{quiz_id}", response_model=schemas.QuizRead)
def get_quiz(quiz_id: int, db: Session = Depends(database.get_db)):
    return quiz_repo.Quiz_read(quiz_id, db)


@router.post("/{Q_id}/submit")
def submit_quiz_answers(Q_id :int, answers: List[schemas.StudentAnswer], db: Session = Depends(database.get_db)):
    return quiz_repo.submit_quiz(Q_id, answers, db)
    
    