from fastapi.testclient import TestClient


def test_register_success(
    client: TestClient,
):
    response = client.post(
        "/register",
        data={
            "email": "user1@example.com",
            "username": "user1",
            "password": "password1234",
            "password_confirm": "password1234",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/dashboard"


def test_register_duplicate_email_fail(
    client: TestClient,
):
    client.post(
        "/register",
        data={
            "email": "user1@example.com",
            "username": "user1",
            "password": "password1234",
            "password_confirm": "password1234",
        },
    )

    response = client.post(
        "/register",
        data={
            "email": "user1@example.com",
            "username": "another",
            "password": "password1234",
            "password_confirm": "password1234",
        },
    )

    assert response.status_code == 400
    assert "이미 가입된 이메일입니다." in response.text


def test_login_success(
    client: TestClient,
):
    client.post(
        "/register",
        data={
            "email": "user1@example.com",
            "username": "user1",
            "password": "password1234",
            "password_confirm": "password1234",
        },
    )

    client.post("/logout")

    response = client.post(
        "/login",
        data={
            "email": "user1@example.com",
            "password": "password1234",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/dashboard"


def test_login_wrong_password_fail(
    client: TestClient,
):
    client.post(
        "/register",
        data={
            "email": "user1@example.com",
            "username": "user1",
            "password": "password1234",
            "password_confirm": "password1234",
        },
    )

    client.post("/logout")

    response = client.post(
        "/login",
        data={
            "email": "user1@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 400
    assert "이메일 또는 비밀번호가 올바르지 않습니다." in response.text


def test_api_requires_login(
    client: TestClient,
):
    response = client.get("/courses")

    assert response.status_code == 401
    assert response.json()["detail"] == "로그인이 필요합니다."