from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_current_user
from app.models import User
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate
from app.services import document_service


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
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    return document_service.get_documents(
        db=db,
        user_id=current_user.id,
        q=q,
        course_id=course_id,
        skip=skip,
        limit=limit,
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