from sqlalchemy.orm import Session
from learning import models, schemas,  database
from fastapi import Depends
from typing import List
   #give access to instructor
def Quiz_create(quiz:schemas.QuizCreate,db:Session = Depends(database.get_db)):
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


def Quiz_read(Q_id:int,db: Session = Depends(database.get_db)):
    get_quiz = db.query(models.Quiz).filter(models.Quiz.Q_id == Q_id).first()
    return get_quiz

# @app.post('enrollment/reviews')
# #registration
# def Review_create(review:schemas.ReviewCreate,db:Session = Depends(database.get_db)):
#     new_Review = models.Reviews(Rating =review.Rating, Rating = review.Rating, review = review.review, E_id = review.E_id)
#     db.add(new_Review)
#     db.commit()
#     db.refresh(new_Review)
#     return new_Review

def Quiz_read_list(Q_id:int,db: Session = Depends(database.get_db)):
    get_quiz = db.query(models.Quiz).all()
    return get_quiz

def submit_quiz(Q_id: int, answers: List[schemas.StudentAnswer], db: Session = Depends(database.get_db)):
    score = 0
    total= len(answers)
    for ans in answers:
        question = db.query(models.Question).filter(models.Question.Qs_id == ans.Qs_id, models.Quiz.Q_id == ans.Q_id).first()
        if question and question.correct_option.upper() == ans.selected_option.upper():
            score += 1
        # Optional: Save each answer
        
    
    return schemas.QuizResult(score = score, total = total)