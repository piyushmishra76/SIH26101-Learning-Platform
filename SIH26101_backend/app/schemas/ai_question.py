from pydantic import BaseModel, Field


class AIQuestionApproval(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str = Field(pattern="^[ABCD]$")
    difficulty: str
    competency_id: int | None = None
    explanation: str | None = None
    source_page: int | None = Field(default=None, ge=1)


class AIQuestionApprovalRequest(BaseModel):
    questions: list[AIQuestionApproval]