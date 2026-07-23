from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course
from app.schemas.course import CourseCreate, CourseUpdate


def create_course(
    db: Session,
    course: CourseCreate,
    user_id: int,
) -> Course:
    existing_course = db.scalar(
        select(Course).where(
            Course.name == course.name,
            Course.user_id == user_id,
        )
    )

    if existing_course is not None:
        raise ValueError("이미 존재하는 과목명입니다.")

    new_course = Course(
        name=course.name,
        description=course.description,
        user_id=user_id,
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


def get_courses(
    db: Session,
    user_id: int,
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Course]:
    statement = select(Course).where(
        Course.user_id == user_id,
    )

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
    user_id: int,
) -> Course | None:
    return db.scalar(
        select(Course).where(
            Course.id == course_id,
            Course.user_id == user_id,
        )
    )


def update_course(
    db: Session,
    course_id: int,
    course_update: CourseUpdate,
    user_id: int,
) -> Course | None:
    course = get_course_by_id(
        db=db,
        course_id=course_id,
        user_id=user_id,
    )

    if course is None:
        return None

    update_data = course_update.model_dump(exclude_unset=True)

    if "name" in update_data:
        if update_data["name"] is None:
            raise ValueError("과목명은 비울 수 없습니다.")

        existing_course = db.scalar(
            select(Course).where(
                Course.name == update_data["name"],
                Course.user_id == user_id,
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
    user_id: int,
) -> bool:
    course = get_course_by_id(
        db=db,
        course_id=course_id,
        user_id=user_id,
    )

    if course is None:
        return False

    db.delete(course)
    db.commit()

    return True