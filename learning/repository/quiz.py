from sqlalchemy.orm import Session
from learning import models, schemas,  database
from fastapi import Depends
from typing import List
   #give access to instructor
def Quiz_create(quiz:schemas.QuizCreate,db:Session):
    new_quiz = models.Quiz( Quiz_name = quiz.Quiz_name )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    for q in quiz.Questions:
        new_question = models.Question(
            # Q_id = new_quiz.Q_id,
            Qs = q.Qs,
            option_a = q.option_a,
            option_b = q.option_b,
            option_c = q.option_c,
            option_d = q.option_d,
            correct_option = q.correct_option.upper(),
            Q_id = new_quiz.Q_id)
        
        db.add(new_question)    
        
    db.commit()   
    return new_quiz


def Quiz_read(Q_id:int,db:Session):
    get_quiz = db.query(models.Quiz).filter(models.Quiz.Q_id == Q_id).first()
    return get_quiz



def Quiz_read_list(db: Session):
    return db.query(models.Quiz).all()

def submit_quiz(Q_id: int, answers: List[schemas.StudentAnswer], db: Session):
    score = 0
    total= len(answers)
    for ans in answers:
        question = db.query(models.Question).filter(models.Question.Qs_id == ans.Qs_id, models.Quiz.Q_id == ans.Q_id).first()
        if question and question.correct_option.upper() == ans.selected_option.upper():
            score += 1
        # Optional: Save each answer
        
    
    return schemas.QuizResult(score = score, total = total)