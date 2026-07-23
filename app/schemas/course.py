from pydantic import BaseModel, ConfigDict, Field

class CourseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        min_length=1,
        max_length=100,
        examples=["데이터통신"],
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        examples=["데이터통신 강의자료를 관리하는 과목"],
    )


class CourseUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        examples=["데이터통신"],
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        examples=["TCP/IP와 네트워크 프로토콜을 공부하는 과목"],
    )

class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    user_id: int