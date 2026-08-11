import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Document, QuizAttempt
from app.schemas.quiz import QuizSubmitItem


STOPWORDS = {
    "그리고",
    "그러나",
    "하지만",
    "또한",
    "따라서",
    "이는",
    "이것은",
    "저것은",
    "있는",
    "한다",
    "된다",
    "대한",
    "위해",
    "통해",
    "에서",
    "으로",
    "에게",
    "이다",
    "있다",
}


def split_sentences(
    content: str,
) -> list[str]:
    sentences = re.split(r"[.!?\n。！？]+", content)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def extract_answer_candidate(
    sentence: str,
    used_answers: set[str],
) -> str | None:
    words = re.findall(
        r"[가-힣A-Za-z0-9]{2,}",
        sentence,
    )

    candidates = []

    for word in words:
        cleaned_word = word.strip()

        if cleaned_word in STOPWORDS:
            continue

        if cleaned_word in used_answers:
            continue

        candidates.append(cleaned_word)

    if not candidates:
        return None

    return max(
        candidates,
        key=len,
    )


def make_blank_question(
    sentence: str,
    answer: str,
) -> str:
    return sentence.replace(
        answer,
        "____",
        1,
    )


def generate_quiz_from_document(
    document: Document,
    limit: int = 5,
) -> list[dict[str, str]]:
    sentences = split_sentences(document.content)

    questions: list[dict[str, str]] = []
    used_answers: set[str] = set()

    for sentence in sentences:
        if len(questions) >= limit:
            break

        answer = extract_answer_candidate(
            sentence=sentence,
            used_answers=used_answers,
        )

        if answer is None:
            continue

        question = make_blank_question(
            sentence=sentence,
            answer=answer,
        )

        if question == sentence:
            continue

        used_answers.add(answer)

        questions.append(
            {
                "question": question,
                "answer": answer,
                "source_sentence": sentence,
            }
        )

    return questions


def normalize_answer(
    answer: str,
) -> str:
    return answer.strip().casefold().replace(" ", "")


def is_correct_answer(
    user_answer: str,
    correct_answer: str,
) -> bool:
    return normalize_answer(user_answer) == normalize_answer(correct_answer)


def submit_quiz_answers(
    db: Session,
    document: Document,
    user_id: int,
    answers: list[QuizSubmitItem],
) -> list[QuizAttempt]:
    attempts: list[QuizAttempt] = []

    for answer_item in answers:
        attempt = QuizAttempt(
            user_id=user_id,
            document_id=document.id,
            question=answer_item.question,
            answer=answer_item.answer,
            user_answer=answer_item.user_answer,
            is_correct=is_correct_answer(
                user_answer=answer_item.user_answer,
                correct_answer=answer_item.answer,
            ),
            source_sentence=answer_item.source_sentence,
        )

        db.add(attempt)
        attempts.append(attempt)

    db.commit()

    for attempt in attempts:
        db.refresh(attempt)

    return attempts


def get_quiz_attempts(
    db: Session,
    user_id: int,
    document_id: int | None = None,
    only_wrong: bool = False,
) -> list[QuizAttempt]:
    statement = select(QuizAttempt).where(
        QuizAttempt.user_id == user_id,
    )

    if document_id is not None:
        statement = statement.where(
            QuizAttempt.document_id == document_id,
        )

    if only_wrong:
        statement = statement.where(
            QuizAttempt.is_correct.is_(False),
        )

    statement = statement.order_by(
        QuizAttempt.id.desc(),
    )

    return list(db.scalars(statement).all())