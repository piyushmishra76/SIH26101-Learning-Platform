from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.Database.connection import get_db
from app.models.competency import Competency
from app.schemas.competency import (
    CompetencyCreate,
    CompetencyResponse
)


router = APIRouter(
    prefix="/competencies",
    tags=["Competencies"]
)


@router.post(
    "/",
    response_model=CompetencyResponse
)
def create_competency(
    competency_data: CompetencyCreate,
    db: Session = Depends(get_db)
):
    existing_competency = (
        db.query(Competency)
        .filter(
            Competency.name == competency_data.name
        )
        .first()
    )

    if existing_competency:
        raise HTTPException(
            status_code=400,
            detail="Competency already exists"
        )

    new_competency = Competency(
        name=competency_data.name,
        description=competency_data.description,
        required_level=competency_data.required_level
    )

    db.add(new_competency)
    db.commit()
    db.refresh(new_competency)

    return new_competency


@router.get(
    "/",
    response_model=list[CompetencyResponse]
)
def get_competencies(
    db: Session = Depends(get_db)
):
    competencies = (
        db.query(Competency)
        .order_by(Competency.id)
        .all()
    )

    return competencies