import sqlite3
from pathlib import Path


# 프로젝트의 최상위 폴더
BASE_DIR = Path(__file__).resolve().parents[1]

# 실제 데이터베이스 파일 경로
DB_PATH = BASE_DIR / "data" / "studyhelper.db"


def print_courses(
    cursor: sqlite3.Cursor,
    title: str,
) -> None:
    """courses 테이블의 전체 데이터를 출력한다."""

    rows = cursor.execute(
        """
        SELECT id, name, description, created_at
        FROM courses
        ORDER BY id
        """
    ).fetchall()

    print(f"\n=== {title} ===")

    if not rows:
        print("저장된 과목이 없습니다.")
        return

    for row in rows:
        print(
            f"id={row['id']}, "
            f"name={row['name']}, "
            f"description={row['description']}, "
            f"created_at={row['created_at']}"
        )


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        # 1. 테이블 생성
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # 반복 실행해도 같은 결과가 나오도록 기존 실습 데이터 삭제
        cursor.execute("DELETE FROM courses")

        # 2. 데이터 생성
        course_data = [
            (
                "데이터통신",
                "네트워크와 데이터 전송 기술을 공부하는 과목",
            ),
            (
                "컴파일러",
                "어휘 분석과 구문 분석을 공부하는 과목",
            ),
            (
                "인공지능",
                "머신러닝과 신경망을 공부하는 과목",
            ),
            (
                "운영체제",
                "프로세스, 스레드, 메모리 관리를 공부하는 과목",
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO courses (name, description)
            VALUES (?, ?)
            """,
            course_data,
        )

        connection.commit()
        print_courses(cursor, "INSERT 이후")

        # 3. 특정 데이터 검색
        search_keyword = "%통신%"

        search_results = cursor.execute(
            """
            SELECT id, name, description
            FROM courses
            WHERE name LIKE ?
            """,
            (search_keyword,),
        ).fetchall()

        print("\n=== '통신' 검색 결과 ===")

        for row in search_results:
            print(dict(row))

        # 4. 데이터 수정
        cursor.execute(
            """
            UPDATE courses
            SET description = ?
            WHERE name = ?
            """,
            (
                "TCP/IP와 네트워크 프로토콜을 공부하는 과목",
                "데이터통신",
            ),
        )

        connection.commit()
        print_courses(cursor, "UPDATE 이후")

        # 5. 데이터 삭제
        cursor.execute(
            """
            DELETE FROM courses
            WHERE name = ?
            """,
            ("인공지능",),
        )

        connection.commit()
        print_courses(cursor, "DELETE 이후")

        # 6. 데이터 개수 조회
        result = cursor.execute(
            """
            SELECT COUNT(*) AS course_count
            FROM courses
            """
        ).fetchone()

        print(f"\n최종 과목 수: {result['course_count']}개")
        print(f"데이터베이스 위치: {DB_PATH}")

    except sqlite3.Error as error:
        connection.rollback()
        print(f"데이터베이스 오류: {error}")
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()