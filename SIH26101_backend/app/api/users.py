from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.Database.connection import get_db
from app.models.user import User
from app.models.competency import Competency, UserCompetency
from app.schemas.competency import (
    UserCompetencyCreate,
    UserCompetencyResponse,
    SkillGapResponse
)
from app.utils.dependencies import get_current_user
from app.services.competency_service import score_to_level


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "designation": current_user.designation,
        "department": current_user.department,
        "education": current_user.education,
        "experience_years": current_user.experience_years,
    }


@router.post(
    "/me/competencies",
    response_model=UserCompetencyResponse
)
def add_or_update_my_competency(
    competency_data: UserCompetencyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    competency = (
        db.query(Competency)
        .filter(
            Competency.id == competency_data.competency_id
        )
        .first()
    )

    if competency is None:
        raise HTTPException(
            status_code=404,
            detail="Competency not found"
        )

    user_competency = (
        db.query(UserCompetency)
        .filter(
            UserCompetency.user_id == current_user.id,
            UserCompetency.competency_id
            == competency_data.competency_id
        )
        .first()
    )

    current_level = score_to_level(
        competency_data.score
    )

    if user_competency:
        user_competency.score = competency_data.score
        user_competency.level = current_level
    else:
        user_competency = UserCompetency(
            user_id=current_user.id,
            competency_id=competency_data.competency_id,
            score=competency_data.score,
            level=current_level
        )

        db.add(user_competency)

    db.commit()
    db.refresh(user_competency)

    return {
        "competency_id": competency.id,
        "competency_name": competency.name,
        "score": user_competency.score,
        "current_level": user_competency.level,
        "required_level": competency.required_level
    }


@router.get(
    "/me/competencies",
    response_model=list[UserCompetencyResponse]
)
def get_my_competencies(
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

    return [
        {
            "competency_id": competency.id,
            "competency_name": competency.name,
            "score": user_competency.score,
            "current_level": user_competency.level,
            "required_level": competency.required_level
        }
        for user_competency, competency in records
    ]


@router.get(
    "/me/skill-gaps",
    response_model=list[SkillGapResponse]
)
def get_my_skill_gaps(
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

    return [
        {
            "competency_id": competency.id,
            "competency_name": competency.name,
            "score": user_competency.score,
            "current_level": user_competency.level,
            "required_level": competency.required_level,
            "gap": max(
                competency.required_level
                - user_competency.level,
                0
            )
        }
        for user_competency, competency in records
    ]