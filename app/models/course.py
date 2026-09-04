from sqlalchemy import Column, Integer, String, Text, Boolean

from app.Database.connection import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey
)
class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    provider = Column(
        String(100),
        nullable=True
    )

    difficulty = Column(
        String(30),
        nullable=False,
        default="beginner"
    )

    duration_hours = Column(
        Integer,
        nullable=True
    )

    source = Column(
        String(50),
        nullable=False,
        default="internal"
    )

    external_url = Column(
        String(500),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )
class CourseCompetency(Base):
    __tablename__ = "course_competencies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    competency_id = Column(
        Integer,
        ForeignKey("competencies.id"),
        nullable=False
    )

    target_level = Column(
        Integer,
        nullable=True
    )