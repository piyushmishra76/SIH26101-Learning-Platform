from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.Database.connection import get_db
from app.models.user import User
from app.models.quiz import Quiz, Question
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    QuestionCreate,
    QuestionResponse
)
from app.utils.dependencies import get_current_user
from app.models.quiz import Quiz, Question, QuizAttempt

from app.models.competency import (
    Competency,
    UserCompetency
)
from app.services.competency_service import score_to_level
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    QuestionCreate,
    QuestionResponse,
    QuizSubmit,
    QuizResultResponse
)
router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)


@router.post(
    "/",
    response_model=QuizResponse
)
def create_quiz(
    quiz_data: QuizCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        created_by=current_user.id
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz

@router.get(
    "/",
    response_model=list[QuizResponse]
)
def get_quizzes(
    db: Session = Depends(get_db)
):
    return (
        db.query(Quiz)
        .filter(Quiz.status == "published")
        .order_by(Quiz.id.desc())
        .all()
    )
@router.get(
    "/{quiz_id}",
    response_model=QuizResponse
)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    quiz = (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id)
        .first()
    )

    if quiz is None:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    return quiz
@router.post(
    "/{quiz_id}/questions",
    response_model=QuestionResponse
)
def add_question(
    quiz_id: int,
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id)
        .first()
    )

    if quiz is None:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    if quiz.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot modify this quiz"
        )

    question = Question(
        quiz_id=quiz_id,
        question_text=question_data.question_text,
        option_a=question_data.option_a,
        option_b=question_data.option_b,
        option_c=question_data.option_c,
        option_d=question_data.option_d,
        correct_answer=question_data.correct_answer,
        difficulty=question_data.difficulty,
        competency_id=question_data.competency_id,
        explanation=question_data.explanation,
        source_page=question_data.source_page
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question
@router.post(
    "/{quiz_id}/submit",
    response_model=QuizResultResponse
)
def submit_quiz(
    quiz_id: int,
    submission: QuizSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.id == quiz_id,
            Quiz.status == "published"
        )
        .first()
    )

    if quiz is None:
        raise HTTPException(
            status_code=404,
            detail="Published quiz not found"
        )

    questions = (
        db.query(Question)
        .filter(
            Question.quiz_id == quiz_id,
            Question.is_active == True
        )
        .all()
    )

    if not questions:
        raise HTTPException(
            status_code=400,
            detail="Quiz has no questions"
        )

    score = 0

    # Store results separately for each competency
    competency_stats = {}

    for question in questions:

        submitted_answer = submission.answers.get(
            question.id
        )

        is_correct = (
            submitted_answer is not None
            and submitted_answer.upper()
            == question.correct_answer.upper()
        )

        if is_correct:
            score += 1

        # Only calculate competency performance
        # when the question has a competency assigned
        if question.competency_id is not None:

            if question.competency_id not in competency_stats:
                competency_stats[question.competency_id] = {
                    "attempted": 0,
                    "correct": 0
                }

            competency_stats[
                question.competency_id
            ]["attempted"] += 1

            if is_correct:
                competency_stats[
                    question.competency_id
                ]["correct"] += 1

    total_questions = len(questions)

    percentage = round(
        (score / total_questions) * 100
    )

    # Save quiz attempt
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score,
        total_questions=total_questions,
        percentage=percentage
    )

    db.add(attempt)

    competency_results = []

    # Update competency scores
    for competency_id, stats in competency_stats.items():

        competency = (
            db.query(Competency)
            .filter(
                Competency.id == competency_id
            )
            .first()
        )

        if competency is None:
            continue

        competency_percentage = round(
            (
                stats["correct"]
                / stats["attempted"]
            ) * 100
        )

        new_level = score_to_level(
            competency_percentage
        )

        user_competency = (
            db.query(UserCompetency)
            .filter(
                UserCompetency.user_id
                == current_user.id,

                UserCompetency.competency_id
                == competency_id
            )
            .first()
        )

        if user_competency:

            user_competency.score = (
                competency_percentage
            )

            user_competency.level = new_level

        else:

            user_competency = UserCompetency(
                user_id=current_user.id,
                competency_id=competency_id,
                score=competency_percentage,
                level=new_level
            )

            db.add(user_competency)

        competency_results.append({
            "competency_id": competency.id,
            "competency_name": competency.name,
            "questions_attempted": stats["attempted"],
            "correct_answers": stats["correct"],
            "percentage": competency_percentage,
            "updated_level": new_level
        })

    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "quiz_id": quiz_id,
        "score": score,
        "total_questions": total_questions,
        "percentage": percentage,
        "competency_results": competency_results
    }
@router.get(
    "/{quiz_id}/questions",
    response_model=list[QuestionResponse]
)
def get_quiz_questions(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.id == quiz_id,
            Quiz.status == "published"
        )
        .first()
    )

    if quiz is None:
        raise HTTPException(
            status_code=404,
            detail="Published quiz not found"
        )

    return (
        db.query(Question)
        .filter(
            Question.quiz_id == quiz_id,
            Question.is_active == True
        )
        .all()
    )