from fastapi import FastAPI
from app.models.user import User
from app.Database.connection import engine, Base
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.models.competency import Competency, UserCompetency
from app.api.competencies import router as competency_router
from app.models.course import Course, CourseCompetency
from app.api.courses import router as course_router
from app.api.documents import router as documents_router
from app.api.ai import router as ai_router
from app.api.recommendations import (

    router as recommendation_router
)
from app.models.document import Document
from app.models.quiz import Quiz, Question, QuizAttempt
from app.models.training import TrainingHistory
from app.api.admin import router as admin_router
from app.api.training import router as training_router  
from app.api.quizzes import router as quiz_router
app = FastAPI(
    title="SIH26101 Learning Platform API",
    description="Backend API for competency-based learning and assessment",
    version="1.0.0"
)
app.include_router(ai_router)
app.include_router(users_router)    
app.include_router(auth_router)
app.include_router(competency_router)
app.include_router(course_router)
app.include_router(recommendation_router)
app.include_router(quiz_router)
app.include_router(admin_router)

app.include_router(documents_router)
app.include_router(training_router)  # Include the training router
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "SIH26101 Backend is running"
    }