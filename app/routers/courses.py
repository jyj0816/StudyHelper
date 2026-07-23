from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_current_user
from app.models import User
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.services import course_service


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(require_current_user)]


@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(
    course: CourseCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    try:
        return course_service.create_course(
            db=db,
            course=course,
            user_id=current_user.id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=list[CourseResponse],
)
def read_courses(
    db: DbSession,
    current_user: CurrentUser,
    q: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    return course_service.get_courses(
        db=db,
        user_id=current_user.id,
        q=q,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def read_course(
    course_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    course = course_service.get_course_by_id(
        db=db,
        course_id=course_id,
        user_id=current_user.id,
    )

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="과목을 찾을 수 없습니다.",
        )

    return course


@router.patch(
    "/{course_id}",
    response_model=CourseResponse,
)
def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    try:
        course = course_service.update_course(
            db=db,
            course_id=course_id,
            course_update=course_update,
            user_id=current_user.id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="과목을 찾을 수 없습니다.",
        )

    return course


@router.delete(
    "/{course_id}",
)
def delete_course(
    course_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    deleted = course_service.delete_course(
        db=db,
        course_id=course_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="과목을 찾을 수 없습니다.",
        )

    return {
        "message": "과목이 삭제되었습니다.",
    }