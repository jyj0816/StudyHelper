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
) -> int:
    response = client.post(
        "/courses",
        json={
            "name": name,
            "description": f"{name} 설명",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_document(
    client: TestClient,
    course_id: int,
) -> int:
    response = client.post(
        "/documents",
        json={
            "title": "프로세스 정리",
            "content": "프로세스는 실행 중인 프로그램입니다. 스레드는 프로세스 안에서 실행되는 작업 단위입니다.",
            "tags": "운영체제, 시험",
            "course_id": course_id,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_generate_document_quiz_api_success(
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
    )
    document_id = create_document(
        client=client,
        course_id=course_id,
    )

    response = client.get(f"/documents/{document_id}/quiz")

    assert response.status_code == 200

    questions = response.json()

    assert len(questions) >= 1
    assert "____" in questions[0]["question"]
    assert questions[0]["answer"]


def test_generate_document_quiz_web_page_success(
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
    )
    document_id = create_document(
        client=client,
        course_id=course_id,
    )

    response = client.get(f"/web/documents/{document_id}/quiz")

    assert response.status_code == 200
    assert "자동 생성 퀴즈" in response.text
    assert "____" in response.text
    assert "정답 보기" in response.text


def test_user_cannot_generate_quiz_for_other_users_document_api(
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
    )
    document_id = create_document(
        client=client,
        course_id=course_id,
    )

    logout(client)

    register_and_login(
        client=client,
        email="user2@example.com",
        username="user2",
    )

    response = client.get(f"/documents/{document_id}/quiz")

    assert response.status_code == 404
    assert response.json()["detail"] == "학습자료를 찾을 수 없습니다."


def test_user_cannot_open_other_users_document_quiz_page(
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
    )
    document_id = create_document(
        client=client,
        course_id=course_id,
    )

    logout(client)

    register_and_login(
        client=client,
        email="user2@example.com",
        username="user2",
    )

    response = client.get(
        f"/web/documents/{document_id}/quiz",
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/web/documents"