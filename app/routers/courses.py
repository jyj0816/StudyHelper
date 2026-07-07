from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.services import course_service


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)


DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(
    course: CourseCreate,
    db: DbSession,
):
    try:
        return course_service.create_course(
            db=db,
            course=course,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=list[CourseResponse],
)
def get_courses(
    db: DbSession,
    q: Annotated[
        str | None,
        Query(min_length=1, max_length=100),
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
    return course_service.get_courses(
        db=db,
        q=q,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def get_course(
    course_id: int,
    db: DbSession,
):
    course = course_service.get_course_by_id(
        db=db,
        course_id=course_id,
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
):
    try:
        course = course_service.update_course(
            db=db,
            course_id=course_id,
            course_update=course_update,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
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
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_course(
    course_id: int,
    db: DbSession,
):
    is_deleted = course_service.delete_course(
        db=db,
        course_id=course_id,
    )

    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="과목을 찾을 수 없습니다.",
        )

    return None