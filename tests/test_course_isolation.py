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


def test_user_can_create_course(
    client: TestClient,
):
    register_and_login(
        client=client,
        email="user1@example.com",
        username="user1",
    )

    response = client.post(
        "/courses",
        json={
            "name": "운영체제",
            "description": "OS 수업",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "운영체제"
    assert data["description"] == "OS 수업"
    assert "user_id" in data


def test_users_only_see_own_courses(
    client: TestClient,
):
    register_and_login(
        client=client,
        email="user1@example.com",
        username="user1",
    )

    client.post(
        "/courses",
        json={
            "name": "운영체제",
            "description": "user1 과목",
        },
    )

    logout(client)

    register_and_login(
        client=client,
        email="user2@example.com",
        username="user2",
    )

    response = client.get("/courses")

    assert response.status_code == 200
    assert response.json() == []


def test_different_users_can_use_same_course_name(
    client: TestClient,
):
    register_and_login(
        client=client,
        email="user1@example.com",
        username="user1",
    )

    response1 = client.post(
        "/courses",
        json={
            "name": "운영체제",
            "description": "user1 과목",
        },
    )

    assert response1.status_code == 201

    logout(client)

    register_and_login(
        client=client,
        email="user2@example.com",
        username="user2",
    )

    response2 = client.post(
        "/courses",
        json={
            "name": "운영체제",
            "description": "user2 과목",
        },
    )

    assert response2.status_code == 201
    assert response2.json()["name"] == "운영체제"


def test_same_user_cannot_create_duplicate_course_name(
    client: TestClient,
):
    register_and_login(
        client=client,
        email="user1@example.com",
        username="user1",
    )

    client.post(
        "/courses",
        json={
            "name": "운영체제",
            "description": "첫 번째",
        },
    )

    response = client.post(
        "/courses",
        json={
            "name": "운영체제",
            "description": "두 번째",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "이미 존재하는 과목명입니다."