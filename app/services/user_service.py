from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserCreate
from app.security import hash_password, verify_password


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return db.scalar(
        select(User).where(User.email == email)
    )


def create_user(
    db: Session,
    user_create: UserCreate,
) -> User:
    existing_user = get_user_by_email(
        db=db,
        email=user_create.email,
    )

    if existing_user is not None:
        raise ValueError("이미 가입된 이메일입니다.")

    user = User(
        email=user_create.email,
        username=user_create.username,
        hashed_password=hash_password(user_create.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        return None

    if not verify_password(
        plain_password=password,
        hashed_password=user.hashed_password,
    ):
        return None

    return user