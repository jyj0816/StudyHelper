from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(
        min_length=1,
        max_length=200,
        examples=["TCP 흐름제어"],
    )

    content: str = Field(
        min_length=1,
        examples=["TCP는 수신 확인과 재전송을 이용하여 신뢰성을 제공한다."],
    )

    tags: str | None = Field(
        default=None,
        max_length=300,
        examples=["TCP, 네트워크, 흐름제어"],
    )

    course_id: int = Field(
        gt=0,
        examples=[1],
    )


class DocumentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        examples=["TCP와 UDP 비교"],
    )

    content: str | None = Field(
        default=None,
        min_length=1,
        examples=["TCP는 연결 지향형이고 UDP는 비연결형이다."],
    )

    tags: str | None = Field(
        default=None,
        max_length=300,
        examples=["TCP, UDP, 프로토콜"],
    )

    course_id: int | None = Field(
        default=None,
        gt=0,
        examples=[1],
    )


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    tags: str | None = None
    course_id: int
    user_id: int