from pydantic import BaseModel, Field


class QuizCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200
    )

    description: str | None = None


class QuizResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_by: int
    status: str

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    question_text: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    correct_answer: str = Field(
        pattern="^[ABCD]$"
    )

    difficulty: str | None = None

    competency_id: int | None = None

    explanation: str | None = None

    source_page: int | None = Field(
        default=None,
        ge=1
    )


class QuestionResponse(BaseModel):
    id: int
    question_text: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    difficulty: str | None
    competency_id: int | None
    explanation: str | None
    source_page: int | None

    class Config:
        from_attributes = True

class QuizSubmit(BaseModel):
    answers: dict[int, str]

class CompetencyQuizResult(BaseModel):
    competency_id: int
    competency_name: str
    questions_attempted: int
    correct_answers: int
    percentage: int
    updated_level: int
class QuizResultResponse(BaseModel):
    attempt_id: int
    quiz_id: int
    score: int
    total_questions: int
    percentage: int
    competency_results: list[CompetencyQuizResult]
