from app.schemas.course import CourseCreate


#DB 연결 전 까지 사용하는 임시 메모리 저장소
_courses: list[dict] = []
_next_course_id = 1


def create_course(course : CourseCreate) -> dict:
    """새로운 과목 생성 저장"""
    global _next_course_id

    new_course = {
        "id": _next_course_id,
        **course.model_dump(),
    }

    _courses.append(new_course)
    _next_course_id +=1

    return new_course

def get_courses(
        q: str | None = None,
        skip: int = 0,
        limit: int = 10,
) -> list[dict]:
    """과목 목록을 검색하고 페이지 단위로 return"""
    filtered_courses = _courses

    if q is not None:
        keyword = q.casefold()

        filtered_courses = [
            course
            for course in _courses
            if keyword in course["name"].casefold()
            or keyword in (course["description"or ""]).casefold()
        ]

    return filtered_courses[skip : skip + limit]

def get_course_by_id(course_id: int) -> dict | None:
    """ID와 일치하는 과목 return"""
    for course in _courses:
        if course["id"] == course_id:
            return course
    
    return None