from pydantic import BaseModel, ConfigDict


class QuizQuestionResponse(BaseModel):
    question: str
    answer: str
    source_sentence: str


class QuizSubmitItem(BaseModel):
    question: str
    answer: str
    source_sentence: str
    user_answer: str


class QuizSubmitRequest(BaseModel):
    answers: list[QuizSubmitItem]


class QuizAttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    question: str
    answer: str
    user_answer: str
    is_correct: bool
    source_sentence: str