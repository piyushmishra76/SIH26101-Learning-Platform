from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.text_preprocessing import clean_text
from app.utils.chunk import chunk_text
from app.services.gemini_service import generate_mcqs
from pathlib import Path
from app.utils.mcq_dedup import remove_duplicate_mcqs
from app.api.documents import UPLOAD_DIR, extract_text_from_pdf
from app.models.quiz import Quiz, Question
from app.utils.dependencies import get_current_trainer_or_admin
from app.Database.connection import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.competency import Competency
from app.Database.connection import get_db
from app.models.quiz import Quiz, Question
from app.schemas.ai_question import AIQuestionApprovalRequest


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class MCQGenerationRequest(BaseModel):
    text: str
    number_of_questions: int = 5


@router.post("/generate-mcqs")
def generate_mcqs_endpoint(
    request: MCQGenerationRequest,
    current_user=Depends(get_current_trainer_or_admin)
    ):

    try:
        mcqs = generate_mcqs(
            request.text,
            request.number_of_questions
        )

        return mcqs

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"MCQ generation failed: {str(e)}"
        )
@router.post("/quizzes/{quiz_id}/approve-mcqs")
def approve_ai_mcqs(
    quiz_id: int,
    request: AIQuestionApprovalRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_trainer_or_admin)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    # Trainer can approve questions only for their own quiz.
    # Admin can approve questions for any quiz.
    if current_user.role != "admin" and quiz.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only approve questions for your own quiz"
        )

    saved_questions = []

    for mcq in request.questions:
        question = Question(
            quiz_id=quiz_id,
            question_text=mcq.question,
            option_a=mcq.option_a,
            option_b=mcq.option_b,
            option_c=mcq.option_c,
            option_d=mcq.option_d,
            correct_answer=mcq.correct_answer,
            difficulty=mcq.difficulty,
            competency_id=mcq.competency_id,
            explanation=mcq.explanation,
            source_page=mcq.source_page
        )

        db.add(question)
        saved_questions.append(question)

    db.commit()

    for question in saved_questions:
        db.refresh(question)

    return {
        "message": "AI-generated questions approved successfully",
        "quiz_id": quiz_id,
        "total_questions": len(saved_questions),
        "questions": saved_questions
    }
@router.post("/generate-mcqs-from-pdf/{filename}")
def generate_mcqs_from_pdf(
    filename: str,
    number_of_questions: int = 5,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_trainer_or_admin)
):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    if file_path.suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    competencies = (
    db.query(Competency)
    .order_by(Competency.id)
    .all()
)

    # 1. Extract text
    raw_text, total_pages = extract_text_from_pdf(file_path)

    if not raw_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from PDF"
        )

    # 2. Clean text
    cleaned_text = clean_text(raw_text)

    # 3. Create chunks
    chunks = chunk_text(cleaned_text)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No chunks were created from PDF"
        )

    # 4. Generate MCQs from chunks
    all_mcqs = []

    total_chunks = len(chunks)

    base_questions = number_of_questions // total_chunks
    remaining_questions = number_of_questions % total_chunks

    for index, chunk in enumerate(chunks):

        questions_for_chunk = base_questions

        if index < remaining_questions:
            questions_for_chunk += 1

        if questions_for_chunk == 0:
            break

        mcqs = generate_mcqs(
        chunk,
        number_of_questions=questions_for_chunk,
        competencies=competencies
)

        all_mcqs.extend(mcqs.questions)
    all_mcqs = all_mcqs[:number_of_questions]
    all_mcqs = remove_duplicate_mcqs(all_mcqs)
    return {
        "filename": filename,
        "total_pages": total_pages,
        "total_chunks": len(chunks),
        "total_questions": len(all_mcqs),
        "questions": all_mcqs
    }
