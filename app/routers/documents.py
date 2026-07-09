from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate
from app.services import document_service


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    document: DocumentCreate,
    db: DbSession,
):
    try:
        return document_service.create_document(
            db=db,
            document=document,
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
def get_documents(
    db: DbSession,
    q: Annotated[
        str | None,
        Query(min_length=1, max_length=100),
    ] = None,
    course_id: Annotated[
        int | None,
        Query(gt=0),
    ] = None,
    skip: Annotated[
        int,
        Query(ge=0),
    ] = 0,
    limit: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 10,
):
    return document_service.get_documents(
        db=db,
        q=q,
        course_id=course_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: DbSession,
):
    document = document_service.get_document_by_id(
        db=db,
        document_id=document_id,
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
):
    try:
        document = document_service.update_document(
            db=db,
            document_id=document_id,
            document_update=document_update,
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
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: int,
    db: DbSession,
):
    is_deleted = document_service.delete_document(
        db=db,
        document_id=document_id,
    )

    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학습자료를 찾을 수 없습니다.",
        )

    return None