import hashlib
import hmac
import secrets


PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 100_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    ).hex()

    return f"{PASSWORD_ALGORITHM}${PASSWORD_ITERATIONS}${salt}${password_hash}"


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    try:
        algorithm, iterations_text, salt, stored_hash = hashed_password.split("$")
        iterations = int(iterations_text)
    except ValueError:
        return False

    if algorithm != PASSWORD_ALGORITHM:
        return False

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    ).hex()

    return hmac.compare_digest(password_hash, stored_hash)