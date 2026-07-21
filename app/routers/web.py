from typing import Annotated

from pathlib import Path

from fastapi import APIRouter, Depends, Form, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseCreate
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.services import course_service, document_service
from app.models import User
from app.services import course_service, document_service, user_service

router = APIRouter(
    tags=["web"],
)

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DbSession = Annotated[Session, Depends(get_db)]

def get_current_user(
    request: Request,
    db: Session,
) -> User | None:
    user_id = request.session.get("user_id")

    if user_id is None:
        return None

    try:
        user_id = int(user_id)
    except ValueError:
        return None

    return user_service.get_user_by_id(
        db=db,
        user_id=user_id,
    )


def redirect_to_login() -> RedirectResponse:
    return RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )

@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard(
    request: Request,
    db: DbSession,
):
    current_user = get_current_user(
        request=request,
        db=db,
    )

    if current_user is None:
        return redirect_to_login()

    courses = course_service.get_courses(
        db=db,
        limit=100,
    )
    documents = document_service.get_documents(
        db=db,
        limit=5,
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "courses": courses,
            "documents": documents,
            "current_user": current_user,
        },
    )


@router.get(
    "/web/courses",
    response_class=HTMLResponse,
)
def course_list(
    request: Request,
    db: DbSession,
):
    courses = course_service.get_courses(
        db=db,
        limit=100,
    )

    return templates.TemplateResponse(
        request=request,
        name="courses/list.html",
        context={
            "courses": courses,
        },
    )


@router.post("/web/courses")
def create_course_from_form(
    db: DbSession,
    name: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
):
    course = CourseCreate(
        name=name,
        description=description,
    )

    try:
        course_service.create_course(
            db=db,
            course=course,
        )
    except ValueError:
        pass

    return RedirectResponse(
        url="/web/courses",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/web/courses/{course_id}/delete")
def delete_course_from_form(
    course_id: int,
    db: DbSession,
):
    course_service.delete_course(
        db=db,
        course_id=course_id,
    )

    return RedirectResponse(
        url="/web/courses",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "/web/documents",
    response_class=HTMLResponse,
)
def document_list(
    request: Request,
    db: DbSession,
    q: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    course_id: Annotated[str | None, Query()] = None,
):
    courses = course_service.get_courses(
        db=db,
        limit=100,
    )

    selected_course_id: int | None = None

    if course_id is not None and course_id.strip() != "":
        try:
            selected_course_id = int(course_id)
        except ValueError:
            selected_course_id = None

    documents = document_service.get_documents(
        db=db,
        q=q,
        course_id=selected_course_id,
        limit=100,
    )

    return templates.TemplateResponse(
        request=request,
        name="documents/list.html",
        context={
            "courses": courses,
            "documents": documents,
            "q": q or "",
            "selected_course_id": selected_course_id,
        },
    )

@router.get(
    "/web/documents/new",
    response_class=HTMLResponse,
)
def document_create_page(
    request: Request,
    db: DbSession,
):
    courses = course_service.get_courses(
        db=db,
        limit=100,
    )

    return templates.TemplateResponse(
        request=request,
        name="documents/new.html",
        context={
            "courses": courses,
        },
    )


@router.post("/web/documents")
def create_document_from_form(
    db: DbSession,
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    tags: Annotated[str | None, Form()] = None,
    course_id: Annotated[int, Form()] = 1,
):
    document = DocumentCreate(
        title=title,
        content=content,
        tags=tags,
        course_id=course_id,
    )

    try:
        document_service.create_document(
            db=db,
            document=document,
        )
    except ValueError:
        return RedirectResponse(
            url="/web/documents/new",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return RedirectResponse(
        url="/web/documents",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "/web/documents/{document_id}",
    response_class=HTMLResponse,
)
def document_detail(
    document_id: int,
    request: Request,
    db: DbSession,
):
    document = document_service.get_document_by_id(
        db=db,
        document_id=document_id,
    )

    if document is None:
        return RedirectResponse(
            url="/web/documents",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return templates.TemplateResponse(
        request=request,
        name="documents/detail.html",
        context={
            "document": document,
        },
    )


@router.get(
    "/web/documents/{document_id}/edit",
    response_class=HTMLResponse,
)
def document_edit_page(
    document_id: int,
    request: Request,
    db: DbSession,
):
    document = document_service.get_document_by_id(
        db=db,
        document_id=document_id,
    )
    courses = course_service.get_courses(
        db=db,
        limit=100,
    )

    if document is None:
        return RedirectResponse(
            url="/web/documents",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return templates.TemplateResponse(
        request=request,
        name="documents/edit.html",
        context={
            "document": document,
            "courses": courses,
        },
    )


@router.post("/web/documents/{document_id}/edit")
def update_document_from_form(
    document_id: int,
    db: DbSession,
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    tags: Annotated[str | None, Form()] = None,
    course_id: Annotated[int, Form()] = 1,
):
    document_update = DocumentUpdate(
        title=title,
        content=content,
        tags=tags,
        course_id=course_id,
    )

    document_service.update_document(
        db=db,
        document_id=document_id,
        document_update=document_update,
    )

    return RedirectResponse(
        url=f"/web/documents/{document_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/web/documents/{document_id}/delete")
def delete_document_from_form(
    document_id: int,
    db: DbSession,
):
    document_service.delete_document(
        db=db,
        document_id=document_id,
    )

    return RedirectResponse(
        url="/web/documents",
        status_code=status.HTTP_303_SEE_OTHER,
    )