from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate
from app.services import user_service


router = APIRouter(
    tags=["auth"],
)

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="auth/register.html",
        context={
            "error": None,
        },
    )


@router.post("/register")
def register(
    request: Request,
    db: DbSession,
    email: Annotated[str, Form()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password_confirm: Annotated[str, Form()],
):
    if password != password_confirm:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={
                "error": "비밀번호가 일치하지 않습니다.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = user_service.create_user(
            db=db,
            user_create=UserCreate(
                email=email,
                username=username,
                password=password,
            ),
        )
    except ValueError as error:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={
                "error": str(error),
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    request.session["user_id"] = user.id

    return RedirectResponse(
        url="/dashboard",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "error": None,
        },
    )


@router.post("/login")
def login(
    request: Request,
    db: DbSession,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    user = user_service.authenticate_user(
        db=db,
        email=email,
        password=password,
    )

    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={
                "error": "이메일 또는 비밀번호가 올바르지 않습니다.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    request.session["user_id"] = user.id

    return RedirectResponse(
        url="/dashboard",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/logout")
def logout(
    request: Request,
):
    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )