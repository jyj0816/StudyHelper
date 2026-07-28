from fastapi.testclient import TestClient


def register_and_login(
    client: TestClient,
    email: str,
    username: str,
):
    client.post(
        "/register",
        data={
            "email": email,
            "username": username,
            "password": "password1234",
            "password_confirm": "password1234",
        },
    )


def logout(
    client: TestClient,
):
    client.post("/logout")


def create_course(
    client: TestClient,
    name: str,
    description: str,
) -> int:
    response = client.post(
        "/courses",
        json={
            "name": name,
            "description": description,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_course_edit_page_success(
    client: TestClient,
):
    register_and_login(
        client=client,
        email="user1@example.com",
        username="user1",
    )

    course_id = create_course(
        client=client,
        name="운영체제",
        description="OS 수업",
    )

    response = client.get(f"/web/courses/{course_id}/edit")

    assert response.status_code == 200
    assert "과목 수정" in response.text
    assert "운영체제" in response.text


def test_update_course_from_web_success(
    client: TestClient,
):
    register_and_login(
        client=client,
        email="user1@example.com",
        username="user1",
    )

    course_id = create_course(
        client=client,
        name="운영체제",
        description="OS 수업",
    )

    response = client.post(
        f"/web/courses/{course_id}/edit",
        data={
            "name": "컴퓨터구조",
            "description": "컴구 수업",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/web/courses"

    courses_response = client.get("/courses")
    courses = courses_response.json()

    assert courses[0]["name"] == "컴퓨터구조"
    assert courses[0]["description"] == "컴구 수업"


def test_update_course_duplicate_name_fail(
    client: TestClient,
):
    register_and_login(
        client=client,
        email="user1@example.com",
        username="user1",
    )

    create_course(
        client=client,
        name="운영체제",
        description="OS 수업",
    )

    course_id = create_course(
        client=client,
        name="자료구조",
        description="DS 수업",
    )

    response = client.post(
        f"/web/courses/{course_id}/edit",
        data={
            "name": "운영체제",
            "description": "이름 중복 테스트",
        },
    )

    assert response.status_code == 400
    assert "이미 존재하는 과목명입니다." in response.text


def test_user_cannot_open_other_users_course_edit_page(
    client: TestClient,
):
    register_and_login(
        client=client,
        email="user1@example.com",
        username="user1",
    )

    course_id = create_course(
        client=client,
        name="운영체제",
        description="user1 과목",
    )

    logout(client)

    register_and_login(
        client=client,
        email="user2@example.com",
        username="user2",
    )

    response = client.get(
        f"/web/courses/{course_id}/edit",
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/web/courses"