from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.Database.connection import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse
from app.models.course import Course, CourseCompetency
from app.models.competency import Competency
from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseCompetencyCreate
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post(
    "/",
    response_model=CourseResponse
)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db)
):
    course = Course(
        title=course_data.title,
        description=course_data.description,
        provider=course_data.provider,
        difficulty=course_data.difficulty,
        duration_hours=course_data.duration_hours,
        source=course_data.source,
        external_url=course_data.external_url
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


@router.get(
    "/",
    response_model=list[CourseResponse]
)
def get_courses(
    db: Session = Depends(get_db)
):
    return (
        db.query(Course)
        .filter(Course.is_active == True)
        .order_by(Course.id)
        .all()
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponse
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course

@router.post("/{course_id}/competencies")
def add_course_competency(
    course_id: int,
    mapping: CourseCompetencyCreate,
    db: Session = Depends(get_db)
):
    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    competency = (
        db.query(Competency)
        .filter(
            Competency.id == mapping.competency_id
        )
        .first()
    )

    if competency is None:
        raise HTTPException(
            status_code=404,
            detail="Competency not found"
        )

    existing_mapping = (
        db.query(CourseCompetency)
        .filter(
            CourseCompetency.course_id == course_id,
            CourseCompetency.competency_id
            == mapping.competency_id
        )
        .first()
    )

    if existing_mapping:
        raise HTTPException(
            status_code=400,
            detail="Course already mapped to this competency"
        )

    new_mapping = CourseCompetency(
        course_id=course_id,
        competency_id=mapping.competency_id,
        target_level=mapping.target_level
    )

    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)

    return {
        "message": "Course mapped to competency successfully",
        "course_id": course_id,
        "competency_id": mapping.competency_id,
        "target_level": mapping.target_level
    }