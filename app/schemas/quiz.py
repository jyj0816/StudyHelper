from pydantic import BaseModel

class QuizQuestionResponse(BaseModel):
    question: str
    answer: str
    source_sentence: str