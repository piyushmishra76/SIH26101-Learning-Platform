from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.Database.connection import get_db
from app.models.user import User
from app.models.competency import Competency, UserCompetency
from app.models.course import Course, CourseCompetency
from app.schemas.recommendation import RecommendationResponse
from app.utils.dependencies import get_current_user
from app.models.training import TrainingHistory
from app.services.recommendation_service import (
    calculate_recommendation_score
)


router = APIRouter(
    prefix="/users/me/recommendations",
    tags=["Recommendations"]
)


@router.get(
    "/",
    response_model=list[RecommendationResponse]
)
def get_my_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = (
        db.query(
            UserCompetency,
            Competency
        )
        .join(
            Competency,
            UserCompetency.competency_id
            == Competency.id
        )
        .filter(
            UserCompetency.user_id == current_user.id
        )
        .all()
    )

    recommendations = []

    for user_competency, competency in records:

        gap = max(
            competency.required_level
            - user_competency.level,
            0
        )

        # No gap means no immediate recommendation
        if gap == 0:
            continue

        courses = (
            db.query(
                Course,
                CourseCompetency
            )
            .join(
                CourseCompetency,
                Course.id
                == CourseCompetency.course_id
            )
            .filter(
                CourseCompetency.competency_id
                == competency.id,
                Course.is_active == True
            )
            .all()
        )

        for course, mapping in courses:

            target_level = (
                mapping.target_level
                or competency.required_level
            )

            score = calculate_recommendation_score(
                gap=gap,
                current_level=user_competency.level,
                target_level=target_level
            )

            if gap >= 3:
                priority = "HIGH"
            elif gap == 2:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            reason = (
                f"Your {competency.name} competency is "
                f"currently at level "
                f"{user_competency.level}, while the "
                f"required level is "
                f"{competency.required_level}."
            )
            completed = (
                db.query(TrainingHistory)
                .filter(
                    TrainingHistory.user_id == current_user.id,
                    TrainingHistory.course_id == course.id,
                    TrainingHistory.status == "completed"
                )
                .first()
            )

            if completed:
                continue
            recommendations.append({
                "course_id": course.id,
                "course_title": course.title,
                "provider": course.provider,
                "difficulty": course.difficulty,
                "competency": competency.name,
                "current_level": user_competency.level,
                "required_level": competency.required_level,
                "gap": gap,
                "score": score,
                "priority": priority,
                "reason": reason
            })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:5]