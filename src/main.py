from fastapi import FastAPI
# from src.routers import auth, students, instructors, results, quizes, questions, modules, courses, contents
from .database import create_db_and_tables, engine, SessionLocal
from src.apps.course.routes import router as course_router
from src.apps.instructor.routes import router as instructor_router
from src.apps.user.routes import router as user_router
from src.apps.auth.routes import router as auth_router
from src.apps.public.routes import router as public_router
from src.apps.student.routes import router as student_router
from src.apps.quiz.routes import router as quiz_router
from src.apps.Result.routes import router as result_router
from src.apps.content.routes import router as content_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# app.include_router(auth.router)
# app.include_router(students.router)
# app.include_router(instructors.router)
# app.include_router(results.router)
# app.include_router(quizes.router)
# app.include_router(modules.router)
# app.include_router(courses.router)
# app.include_router(contents.router)
# app.include_router(questions.router)

app.include_router(auth_router)
app.include_router(public_router)
app.include_router(course_router)
app.include_router(instructor_router)
app.include_router(user_router)
app.include_router(student_router)
app.include_router(quiz_router)
app.include_router(result_router)
app.include_router(content_router)