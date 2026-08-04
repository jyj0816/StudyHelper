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
    title: str,
    content: str,
    tags: str,
    course_id: int,
):
    response = client.post(
        "/documents",
        json={
            "title": title,
            "content": content,
            "tags": tags,
            "course_id": course_id,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_document_tags_are_normalized(
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

    document = create_document(
        client=client,
        title="프로세스 정리",
        content="프로세스와 스레드 내용",
        tags=" 시험, #운영체제, 시험 ",
        course_id=course_id,
    )

    assert document["tags"] == "시험, 운영체제"


def test_document_search_by_keyword(
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

    create_document(
        client=client,
        title="프로세스 정리",
        content="프로세스와 스레드 내용",
        tags="운영체제, 시험",
        course_id=course_id,
    )
    create_document(
        client=client,
        title="SQL 정리",
        content="SELECT와 JOIN 내용",
        tags="데이터베이스",
        course_id=course_id,
    )

    response = client.get("/documents?q=프로세스")

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 1
    assert documents[0]["title"] == "프로세스 정리"


def test_document_filter_by_tag(
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

    create_document(
        client=client,
        title="중간고사 정리",
        content="시험 범위 정리",
        tags="시험, 운영체제",
        course_id=course_id,
    )
    create_document(
        client=client,
        title="과제 메모",
        content="과제 내용",
        tags="과제",
        course_id=course_id,
    )

    response = client.get("/documents?tag=시험")

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 1
    assert documents[0]["title"] == "중간고사 정리"


def test_document_web_page_shows_tag_links(
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

    create_document(
        client=client,
        title="프로세스 정리",
        content="프로세스와 스레드 내용",
        tags="운영체제, 시험",
        course_id=course_id,
    )

    response = client.get("/web/documents")

    assert response.status_code == 200
    assert "#운영체제" in response.text
    assert "#시험" in response.text


def test_document_web_page_filters_by_tag(
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

    create_document(
        client=client,
        title="중간고사 정리",
        content="시험 범위 정리",
        tags="시험",
        course_id=course_id,
    )
    create_document(
        client=client,
        title="과제 메모",
        content="과제 내용",
        tags="과제",
        course_id=course_id,
    )

    response = client.get("/web/documents?tag=시험")

    assert response.status_code == 200
    assert "중간고사 정리" in response.text
    assert "과제 메모" not in response.text