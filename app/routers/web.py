from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models import User
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.services import course_service, document_service


router = APIRouter(
    tags=["web"],
)

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DbSession = Annotated[Session, Depends(get_db)]


def redirect_to_login() -> RedirectResponse:
    return RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )


def require_web_user(
    request: Request,
    db: Session,
) -> User | RedirectResponse:
    current_user = get_current_user(
        request=request,
        db=db,
    )

    if current_user is None:
        return redirect_to_login()

    return current_user


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard(
    request: Request,
    db: DbSession,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    courses = course_service.get_courses(
        db=db,
        user_id=current_user.id,
        limit=100,
    )
    documents = document_service.get_documents(
        db=db,
        user_id=current_user.id,
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
    q: str | None = None,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    courses = course_service.get_courses(
        db=db,
        user_id=current_user.id,
        q=q,
        limit=100,
    )

    return templates.TemplateResponse(
        request=request,
        name="courses/list.html",
        context={
            "courses": courses,
            "q": q or "",
            "error": None,
            "current_user": current_user,
        },
    )


@router.post(
    "/web/courses",
)
def create_course_from_web(
    request: Request,
    db: DbSession,
    name: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    try:
        from app.schemas.course import CourseCreate

        course_service.create_course(
            db=db,
            course=CourseCreate(
                name=name,
                description=description,
            ),
            user_id=current_user.id,
        )
    except ValueError as error:
        courses = course_service.get_courses(
            db=db,
            user_id=current_user.id,
            limit=100,
        )

        return templates.TemplateResponse(
            request=request,
            name="courses/list.html",
            context={
                "courses": courses,
                "q": "",
                "error": str(error),
                "current_user": current_user,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
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
    q: str | None = None,
    course_id: str | None = None,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    selected_course_id: int | None = None

    if course_id not in (None, ""):
        selected_course_id = int(course_id)

    courses = course_service.get_courses(
        db=db,
        user_id=current_user.id,
        limit=100,
    )
    documents = document_service.get_documents(
        db=db,
        user_id=current_user.id,
        q=q,
        course_id=selected_course_id,
        limit=100,
    )

    return templates.TemplateResponse(
        request=request,
        name="documents/list.html",
        context={
            "documents": documents,
            "courses": courses,
            "q": q or "",
            "selected_course_id": selected_course_id,
            "current_user": current_user,
        },
    )


@router.get(
    "/web/documents/new",
    response_class=HTMLResponse,
)
def new_document_page(
    request: Request,
    db: DbSession,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    courses = course_service.get_courses(
        db=db,
        user_id=current_user.id,
        limit=100,
    )

    return templates.TemplateResponse(
        request=request,
        name="documents/new.html",
        context={
            "courses": courses,
            "error": None,
            "current_user": current_user,
        },
    )


@router.post(
    "/web/documents",
)
def create_document_from_web(
    request: Request,
    db: DbSession,
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    course_id: Annotated[int, Form()],
    tags: Annotated[str | None, Form()] = None,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    try:
        document = document_service.create_document(
            db=db,
            document=DocumentCreate(
                title=title,
                content=content,
                course_id=course_id,
                tags=tags,
            ),
            user_id=current_user.id,
        )
    except ValueError as error:
        courses = course_service.get_courses(
            db=db,
            user_id=current_user.id,
            limit=100,
        )

        return templates.TemplateResponse(
            request=request,
            name="documents/new.html",
            context={
                "courses": courses,
                "error": str(error),
                "current_user": current_user,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return RedirectResponse(
        url=f"/web/documents/{document.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )



@router.post(
    "/web/courses/{course_id}/delete",
)
def delete_course_from_web(
    course_id: int,
    request: Request,
    db: DbSession,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    course_service.delete_course(
        db=db,
        course_id=course_id,
        user_id=current_user.id,
    )

    return RedirectResponse(
        url="/web/courses",
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
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    document = document_service.get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
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
            "current_user": current_user,
        },
    )


@router.get(
    "/web/documents/{document_id}/edit",
    response_class=HTMLResponse,
)
def edit_document_page(
    document_id: int,
    request: Request,
    db: DbSession,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    document = document_service.get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

    if document is None:
        return RedirectResponse(
            url="/web/documents",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    courses = course_service.get_courses(
        db=db,
        user_id=current_user.id,
        limit=100,
    )

    return templates.TemplateResponse(
        request=request,
        name="documents/edit.html",
        context={
            "document": document,
            "courses": courses,
            "error": None,
            "current_user": current_user,
        },
    )


@router.post(
    "/web/documents/{document_id}/edit",
)
def update_document_from_web(
    document_id: int,
    request: Request,
    db: DbSession,
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    course_id: Annotated[int, Form()],
    tags: Annotated[str | None, Form()] = None,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    try:
        document = document_service.update_document(
            db=db,
            document_id=document_id,
            document_update=DocumentUpdate(
                title=title,
                content=content,
                course_id=course_id,
                tags=tags,
            ),
            user_id=current_user.id,
        )
    except ValueError as error:
        old_document = document_service.get_document_by_id(
            db=db,
            document_id=document_id,
            user_id=current_user.id,
        )
        courses = course_service.get_courses(
            db=db,
            user_id=current_user.id,
            limit=100,
        )

        return templates.TemplateResponse(
            request=request,
            name="documents/edit.html",
            context={
                "document": old_document,
                "courses": courses,
                "error": str(error),
                "current_user": current_user,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if document is None:
        return RedirectResponse(
            url="/web/documents",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return RedirectResponse(
        url=f"/web/documents/{document.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post(
    "/web/documents/{document_id}/delete",
)
def delete_document_from_web(
    document_id: int,
    request: Request,
    db: DbSession,
):
    current_user = require_web_user(
        request=request,
        db=db,
    )

    if isinstance(current_user, RedirectResponse):
        return current_user

    document_service.delete_document(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

    return RedirectResponse(
        url="/web/documents",
        status_code=status.HTTP_303_SEE_OTHER,
    )