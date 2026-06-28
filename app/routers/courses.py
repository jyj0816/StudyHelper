from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.course import CourseCreate, CourseResponse


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)


# DB 구현 전까지 사용할 임시 메모리 저장소
courses: list[dict] = []
next_course_id = 1


@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(course: CourseCreate):
    global next_course_id

    new_course = {
        "id": next_course_id,
        **course.model_dump(),
    }

    courses.append(new_course)
    next_course_id += 1

    return new_course


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
    filtered_courses = courses

    if q is not None:
        keyword = q.lower()

        filtered_courses = [
            course
            for course in courses
            if keyword in course["name"].lower()
            or (
                course["description"] is not None
                and keyword in course["description"].lower()
            )
        ]

    return filtered_courses[skip : skip + limit]


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="과목을 찾을 수 없습니다.",
    )