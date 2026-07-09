from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course, Document
from app.schemas.document import DocumentCreate, DocumentUpdate


def create_document(
    db: Session,
    document: DocumentCreate,
) -> Document:
    """새로운 학습자료를 데이터베이스에 생성한다."""

    course = db.get(Course, document.course_id)

    if course is None:
        raise ValueError("존재하지 않는 과목입니다.")

    new_document = Document(
        title=document.title,
        content=document.content,
        tags=document.tags,
        course_id=document.course_id,
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


def get_documents(
    db: Session,
    q: str | None = None,
    course_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Document]:
    """학습자료 목록을 검색하고 페이지 단위로 반환한다."""

    statement = select(Document)

    if course_id is not None:
        statement = statement.where(Document.course_id == course_id)

    if q is not None:
        keyword = f"%{q}%"

        statement = statement.where(
            Document.title.like(keyword)
            | Document.content.like(keyword)
            | Document.tags.like(keyword)
        )

    statement = (
        statement
        .order_by(Document.id.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def get_document_by_id(
    db: Session,
    document_id: int,
) -> Document | None:
    """ID와 일치하는 학습자료를 반환한다."""

    return db.get(Document, document_id)


def update_document(
    db: Session,
    document_id: int,
    document_update: DocumentUpdate,
) -> Document | None:
    """학습자료를 수정한다."""

    document = get_document_by_id(
        db=db,
        document_id=document_id,
    )

    if document is None:
        return None

    update_data = document_update.model_dump(exclude_unset=True)

    if "course_id" in update_data:
        course_id = update_data["course_id"]

        if course_id is None:
            raise ValueError("과목 ID는 비울 수 없습니다.")

        course = db.get(Course, course_id)

        if course is None:
            raise ValueError("존재하지 않는 과목입니다.")

    for field, value in update_data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)

    return document


def delete_document(
    db: Session,
    document_id: int,
) -> bool:
    """학습자료를 삭제한다."""

    document = get_document_by_id(
        db=db,
        document_id=document_id,
    )

    if document is None:
        return False

    db.delete(document)
    db.commit()

    return True