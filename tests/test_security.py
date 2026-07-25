from app.security import hash_password, verify_password


def test_hash_password_does_not_store_plain_text():
    password = "password1234"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert "password1234" not in hashed_password


def test_verify_password_success():
    password = "password1234"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_fail():
    password = "password1234"
    hashed_password = hash_password(password)

    assert verify_password("wrongpassword", hashed_password) is False