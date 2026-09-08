from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.Database.connection import get_db
from app.models.training import TrainingHistory
from app.models.course import Course
from app.models.quiz import QuizAttempt 
from app.models.user import User
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/training",
    tags=["Training"]
)


@router.post("/enroll/{course_id}")
def enroll_in_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # 1. Check whether course exists
    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.is_active == True
        )
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found or inactive"
        )

    # 2. Check whether user is already enrolled
    existing_training = (
        db.query(TrainingHistory)
        .filter(
            TrainingHistory.user_id == current_user.id,
            TrainingHistory.course_id == course_id
        )
        .first()
    )

    if existing_training:
        raise HTTPException(
            status_code=400,
            detail="You are already enrolled in this course"
        )

    # 3. Create training record
    training = TrainingHistory(
        user_id=current_user.id,
        course_id=course_id,
        status="enrolled",
        completion_percentage=0
    )

    db.add(training)
    db.commit()
    db.refresh(training)

    return {
        "message": "Course enrolled successfully",
        "training_id": training.id,
        "course_id": course.id,
        "course_title": course.title,
        "status": training.status,
        "completion_percentage": training.completion_percentage,
        "enrolled_at": training.created_at
    }

@router.patch("/{training_id}/progress")
def update_training_progress(
    training_id: int,
    completion_percentage: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    training = (
        db.query(TrainingHistory)
        .filter(
            TrainingHistory.id == training_id,
            TrainingHistory.user_id == current_user.id
        )
        .first()
    )

    if not training:
        raise HTTPException(
            status_code=404,
            detail="Training record not found"
        )

    # 1. validate completion_percentage
    if completion_percentage<0 or completion_percentage>100:
        raise HTTPException(
            status_code=400,
            detail="Completion percentage must be between 0 and 100"
        )
    elif completion_percentage == 100:
        status = "completed"
        completed_at = datetime.now()
    else:
        status = "in_progress"
        completed_at = None
    training.completion_percentage = completion_percentage
    training.status = status
    training.completed_at = completed_at
    db.commit()
    db.refresh(training)
    return {
        "message": "Training progress updated successfully",
        "training_id": training.id,
        "course_id": training.course_id,
        "status": training.status,  
        "completion_percentage": training.completion_percentage,
        "completed_at": training.completed_at
    }
@router.get("/my-history")
def get_my_current_history(
    current_user:User=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    history=(
        db.query(TrainingHistory,Course)
        .join(Course, TrainingHistory.course_id == Course.id)
        .filter(TrainingHistory.user_id==current_user.id)
        .all()
    )
    result=[]
    for training,course in history:
        result.append(
            {
                "training_id":training.id,
                "course_id":course.id,
                "course_title":course.title,
                "status":training.status,
                "completion_percentage":training.completion_percentage,
                "enrolled_at":training.created_at,
                "completed_at":training.completed_at
            }
        )
    return result
@router.get("/analytics")
def get_learning_analytics(
    current_user: User = Depends(get_current_user),
    db:Session=Depends(get_db)
):
    total_courses=(
        db.query(TrainingHistory)
        .filter(TrainingHistory.user_id==current_user.id)
        .count()
    )
    completed_courses=(
        db.query(TrainingHistory)
        .filter(
            TrainingHistory.user_id==current_user.id,
            TrainingHistory.status=="completed"
        )
        .count()
    )
    in_progress_courses=(
        db.query(TrainingHistory)
        .filter(
            TrainingHistory.user_id==current_user.id,
            TrainingHistory.status=="in_progress"
        )
        .count()
    )
    avg_progress=db.query(func.avg(TrainingHistory.completion_percentage))
    # -------------------------
    # Quiz Analytics
    # -------------------------

    quizzes_attempted = (
        db.query(QuizAttempt)
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .count()
    )

    average_quiz_percentage = (
        db.query(
            func.avg(QuizAttempt.percentage)
        )
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .scalar()
        or 0
    )

    # -------------------------
    # Final Response
    # -------------------------

    return {
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "in_progress_courses": in_progress_courses,
        "average_progress": avg_progress,
        "quizzes_attempted": quizzes_attempted,
        "average_quiz_percentage": average_quiz_percentage
    }