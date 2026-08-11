from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_current_user
from app.models import User
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate
from app.schemas.quiz import (
    QuizAttemptResponse,
    QuizQuestionResponse,
    QuizSubmitRequest,
)
from app.services import document_service, quiz_service


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(require_current_user)]


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    document: DocumentCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    try:
        return document_service.create_document(
            db=db,
            document=document,
            user_id=current_user.id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def read_documents(
    db: DbSession,
    current_user: CurrentUser,
    q: str | None = Query(default=None),
    course_id: int | None = Query(default=None),
    tag: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    return document_service.get_documents(
        db=db,
        user_id=current_user.id,
        q=q,
        course_id=course_id,
        tag=tag,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{document_id}/quiz",
    response_model=list[QuizQuestionResponse],
)
def generate_document_quiz(
    document_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    document = document_service.get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학습자료를 찾을 수 없습니다.",
        )

    return quiz_service.generate_quiz_from_document(
        document=document,
    )

@router.post(
    "/{document_id}/quiz/submit",
    response_model=list[QuizAttemptResponse],
)
def submit_document_quiz(
    document_id: int,
    quiz_submit: QuizSubmitRequest,
    db: DbSession,
    current_user: CurrentUser,
):
    document = document_service.get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학습자료를 찾을 수 없습니다.",
        )

    return quiz_service.submit_quiz_answers(
        db=db,
        document=document,
        user_id=current_user.id,
        answers=quiz_submit.answers,
    )


@router.get(
    "/quiz/wrong-notes",
    response_model=list[QuizAttemptResponse],
)
def read_wrong_notes(
    db: DbSession,
    current_user: CurrentUser,
):
    return quiz_service.get_quiz_attempts(
        db=db,
        user_id=current_user.id,
        only_wrong=True,
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def read_document(
    document_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    document = document_service.get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학습자료를 찾을 수 없습니다.",
        )

    return document


@router.patch(
    "/{document_id}",
    response_model=DocumentResponse,
)
def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    try:
        document = document_service.update_document(
            db=db,
            document_id=document_id,
            document_update=document_update,
            user_id=current_user.id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학습자료를 찾을 수 없습니다.",
        )

    return document


@router.delete(
    "/{document_id}",
)
def delete_document(
    document_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    deleted = document_service.delete_document(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학습자료를 찾을 수 없습니다.",
        )

    return {
        "message": "학습자료가 삭제되었습니다.",
    }