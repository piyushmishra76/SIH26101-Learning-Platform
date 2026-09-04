from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    course_id: int
    course_title: str
    provider: str | None
    difficulty: str
    competency: str
    current_level: int
    required_level: int
    gap: int
    score: float
    priority: str
    reason: str