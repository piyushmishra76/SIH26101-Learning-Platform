from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    email: EmailStr

    password: str = Field(min_length=8, max_length=100)

    designation: str | None = None

    department: str | None = None

    education: str | None = None

    experience_years: int | None = Field(
        default=None,
        ge=0
    )

class UserLogin(BaseModel):
    email: EmailStr
    password: str