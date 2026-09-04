from pydantic import BaseModel, Field


class CompetencyCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    description: str | None = None

    required_level: int = Field(
        default=3,
        ge=1,
        le=5
    )


class CompetencyResponse(BaseModel):
    id: int
    name: str
    description: str | None
    required_level: int

    class Config:
        from_attributes = True

class UserCompetencyCreate(BaseModel):
    competency_id: int = Field(gt=0)

    score: int = Field(
        ge=0,
        le=100
    )


class UserCompetencyResponse(BaseModel):
    competency_id: int
    competency_name: str
    score: int
    current_level: int
    required_level: int


class SkillGapResponse(BaseModel):
    competency_id: int
    competency_name: str
    current_level: int
    required_level: int
    gap: int
    score: int