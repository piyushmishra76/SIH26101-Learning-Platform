from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200
    )

    description: str | None = None

    provider: str | None = None

    difficulty: str = "beginner"

    duration_hours: int | None = Field(
        default=None,
        ge=1
    )

    source: str = "internal"

    external_url: str | None = None


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str | None
    provider: str | None
    difficulty: str
    duration_hours: int | None
    source: str
    external_url: str | None
    is_active: bool

    class Config:
        from_attributes = True

class CourseCompetencyCreate(BaseModel):
    competency_id: int = Field(gt=0)

    target_level: int | None = Field(
        default=None,
        ge=1,
        le=5
    )