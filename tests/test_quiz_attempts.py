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


def test_submit_document_quiz_api_success(
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

    quiz_response = client.get(f"/documents/{document_id}/quiz")
    quiz = quiz_response.json()

    response = client.post(
        f"/documents/{document_id}/quiz/submit",
        json={
            "answers": [
                {
                    "question": quiz[0]["question"],
                    "answer": quiz[0]["answer"],
                    "source_sentence": quiz[0]["source_sentence"],
                    "user_answer": quiz[0]["answer"],
                }
            ]
        },
    )

    assert response.status_code == 200

    attempts = response.json()

    assert len(attempts) == 1
    assert attempts[0]["is_correct"] is True


def test_submit_document_quiz_api_wrong_answer(
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

    quiz_response = client.get(f"/documents/{document_id}/quiz")
    quiz = quiz_response.json()

    response = client.post(
        f"/documents/{document_id}/quiz/submit",
        json={
            "answers": [
                {
                    "question": quiz[0]["question"],
                    "answer": quiz[0]["answer"],
                    "source_sentence": quiz[0]["source_sentence"],
                    "user_answer": "틀린답",
                }
            ]
        },
    )

    assert response.status_code == 200

    attempts = response.json()

    assert attempts[0]["is_correct"] is False


def test_wrong_notes_api_only_shows_wrong_answers(
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

    quiz_response = client.get(f"/documents/{document_id}/quiz")
    quiz = quiz_response.json()

    client.post(
        f"/documents/{document_id}/quiz/submit",
        json={
            "answers": [
                {
                    "question": quiz[0]["question"],
                    "answer": quiz[0]["answer"],
                    "source_sentence": quiz[0]["source_sentence"],
                    "user_answer": "틀린답",
                }
            ]
        },
    )

    response = client.get("/documents/quiz/wrong-notes")

    assert response.status_code == 200

    wrong_notes = response.json()

    assert len(wrong_notes) == 1
    assert wrong_notes[0]["is_correct"] is False


def test_user_cannot_submit_other_users_document_quiz(
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

    response = client.post(
        f"/documents/{document_id}/quiz/submit",
        json={
            "answers": [
                {
                    "question": "문제",
                    "answer": "정답",
                    "source_sentence": "원문",
                    "user_answer": "정답",
                }
            ]
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "학습자료를 찾을 수 없습니다."


def test_wrong_notes_web_page_success(
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

    quiz_response = client.get(f"/documents/{document_id}/quiz")
    quiz = quiz_response.json()

    client.post(
        f"/documents/{document_id}/quiz/submit",
        json={
            "answers": [
                {
                    "question": quiz[0]["question"],
                    "answer": quiz[0]["answer"],
                    "source_sentence": quiz[0]["source_sentence"],
                    "user_answer": "틀린답",
                }
            ]
        },
    )

    response = client.get("/web/wrong-notes")

    assert response.status_code == 200
    assert "오답노트" in response.text
    assert "틀린답" in response.text