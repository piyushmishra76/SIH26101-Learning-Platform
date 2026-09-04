from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean
)

from app.Database.connection import Base


class Quiz(Base):
    __tablename__ = "quizzes"

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

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="draft"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )

    question_text = Column(
        Text,
        nullable=False
    )

    option_a = Column(
        Text,
        nullable=False
    )

    option_b = Column(
        Text,
        nullable=False
    )

    option_c = Column(
        Text,
        nullable=False
    )

    option_d = Column(
        Text,
        nullable=False
    )

    correct_answer = Column(
        String(1),
        nullable=False
    )

    difficulty = Column(
        String(30),
        nullable=True
    )

    competency_id = Column(
        Integer,
        ForeignKey("competencies.id"),
        nullable=True
    )

    explanation = Column(
        Text,
        nullable=True
    )

    source_page = Column(
        Integer,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

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

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )

    score = Column(
        Integer,
        nullable=False,
        default=0
    )

    total_questions = Column(
        Integer,
        nullable=False
    )

    percentage = Column(
        Integer,
        nullable=False,
        default=0
    )

    attempted_at = Column(
        DateTime,
        default=datetime.utcnow
    )