from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course
from app.schemas.course import CourseCreate, CourseUpdate


def create_course(
    db: Session,
    course: CourseCreate,
) -> Course:
    """새로운 과목을 DB에 생성한다."""

    existing_course = db.scalar(
        select(Course).where(Course.name == course.name)
    )

    if existing_course is not None:
        raise ValueError("이미 존재하는 과목명입니다.")

    new_course = Course(
        name=course.name,
        description=course.description,
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

def get_courses(
    db: Session,
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Course]:
    """과목 목록을 검색하고 페이지 단위로 반환"""

    statement = select(Course)

    if q is not None:
        keyword = f"%{q}%"

        statement = statement.where(
            Course.name.like(keyword)
            | Course.description.like(keyword)
        )

    statement = (
        statement
        .order_by(Course.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def get_course_by_id(
    db: Session,
    course_id: int,
) -> Course | None:
    """ID와 일치하는 과목을 반환"""

    return db.get(Course, course_id)


def update_course(
    db: Session,
    course_id: int,
    course_update: CourseUpdate,
) -> Course | None:
    """과목 정보 수정"""

    course = get_course_by_id(db, course_id)

    if course is None:
        return None

    update_data = course_update.model_dump(exclude_unset=True)

    if "name" in update_data:
        if update_data["name"] is None:
            raise ValueError("과목명은 비울 수 없습니다.")

        existing_course = db.scalar(
            select(Course).where(
                Course.name == update_data["name"],
                Course.id != course_id,
            )
        )

        if existing_course is not None:
            raise ValueError("이미 존재하는 과목명입니다.")

    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)

    return course


def delete_course(
    db: Session,
    course_id: int,
) -> bool:
    """과목 삭제"""

    course = get_course_by_id(db, course_id)

    if course is None:
        return False

    db.delete(course)
    db.commit()

    return True