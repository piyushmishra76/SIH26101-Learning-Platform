from pydantic import BaseModel, Field


class MCQ(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    correct_answer: str = Field(
        pattern="^[ABCD]$"
    )

    difficulty: str
    explanation: str
    source_page: int | None = None
    competency_id: int | None = None


class MCQResponse(BaseModel):
    questions: list[MCQ]