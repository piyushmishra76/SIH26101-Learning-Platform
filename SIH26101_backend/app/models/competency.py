from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)

from app.Database.connection import Base


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    required_level = Column(
        Integer,
        nullable=False,
        default=3
    )


class UserCompetency(Base):
    __tablename__ = "user_competencies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    competency_id = Column(
        Integer,
        ForeignKey("competencies.id"),
        nullable=False
    )

    score = Column(
        Integer,
        nullable=False,
        default=0
    )

    level = Column(
        Integer,
        nullable=False,
        default=1
    )