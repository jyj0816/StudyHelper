from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course, Document
from app.schemas.document import DocumentCreate, DocumentUpdate


def normalize_tags(
    tags: str | None,
) -> str | None:
    if tags is None:
        return None

    tag_items = [
        tag.strip().lstrip("#")
        for tag in tags.split(",")
        if tag.strip()
    ]

    if not tag_items:
        return None

    unique_tags = sorted(set(tag_items))

    return ", ".join(unique_tags)


def create_document(
    db: Session,
    document: DocumentCreate,
    user_id: int,
) -> Document:
    course = db.scalar(
        select(Course).where(
            Course.id == document.course_id,
            Course.user_id == user_id,
        )
    )

    if course is None:
        raise ValueError("존재하지 않는 과목입니다.")

    new_document = Document(
        title=document.title,
        content=document.content,
        tags=normalize_tags(document.tags),
        course_id=document.course_id,
        user_id=user_id,
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


def get_documents(
    db: Session,
    user_id: int,
    q: str | None = None,
    course_id: int | None = None,
    tag: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Document]:
    statement = select(Document).where(
        Document.user_id == user_id,
    )

    if course_id is not None:
        statement = statement.where(
            Document.course_id == course_id,
        )

    if tag is not None and tag.strip():
        keyword = f"%{tag.strip().lstrip('#')}%"

        statement = statement.where(
            Document.tags.like(keyword)
        )

    if q is not None and q.strip():
        keyword = f"%{q.strip()}%"

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


def get_all_tags(
    db: Session,
    user_id: int,
) -> list[str]:
    documents = db.scalars(
        select(Document).where(
            Document.user_id == user_id,
            Document.tags.is_not(None),
        )
    ).all()

    tags: set[str] = set()

    for document in documents:
        if document.tags is None:
            continue

        for tag in document.tags.split(","):
            cleaned_tag = tag.strip()

            if cleaned_tag:
                tags.add(cleaned_tag)

    return sorted(tags)


def get_document_by_id(
    db: Session,
    document_id: int,
    user_id: int,
) -> Document | None:
    return db.scalar(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == user_id,
        )
    )


def update_document(
    db: Session,
    document_id: int,
    document_update: DocumentUpdate,
    user_id: int,
) -> Document | None:
    document = get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=user_id,
    )

    if document is None:
        return None

    update_data = document_update.model_dump(exclude_unset=True)

    if "course_id" in update_data:
        course_id = update_data["course_id"]

        if course_id is None:
            raise ValueError("과목 ID는 비울 수 없습니다.")

        course = db.scalar(
            select(Course).where(
                Course.id == course_id,
                Course.user_id == user_id,
            )
        )

        if course is None:
            raise ValueError("존재하지 않는 과목입니다.")

    if "tags" in update_data:
        update_data["tags"] = normalize_tags(update_data["tags"])

    for field, value in update_data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)

    return document


def delete_document(
    db: Session,
    document_id: int,
    user_id: int,
) -> bool:
    document = get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=user_id,
    )

    if document is None:
        return False

    db.delete(document)
    db.commit()

    return True