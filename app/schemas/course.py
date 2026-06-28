from pydantic import BaseModel, ConfigDict, Field

class CourseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name : str = Field(
        min_length= 1,
        max_length= 100,
        examples=["데이터통신"]
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        examples=["데이터통신 강의자료 관리 목록"]
    )

class CourseResponse(CourseCreate):
    id : int