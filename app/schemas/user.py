from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr = Field(
        examples=["student@example.com"],
    )

    username: str = Field(
        min_length=1,
        max_length=100,
        examples=["jyj0816"],
    )

    password: str = Field(
        min_length=8,
        max_length=100,
        examples=["password1234"],
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str