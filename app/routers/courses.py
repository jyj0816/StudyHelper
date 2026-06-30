from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.course import CourseCreate, CourseResponse
from app.services import course_service


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)


@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(course: CourseCreate):
    return course_service.create_course(course)


@router.get(
    "",
    response_model=list[CourseResponse],
)
def get_courses(
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
        q=q,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def get_course(course_id: int):
    course = course_service.get_course_by_id(course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="과목을 찾을 수 없습니다.",
        )

    return course