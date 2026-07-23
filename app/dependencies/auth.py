from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services import user_service


DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    request: Request,
    db: DbSession,
) -> User | None:
    user_id = request.session.get("user_id")

    if user_id is None:
        return None

    try:
        user_id = int(user_id)
    except ValueError:
        return None

    return user_service.get_user_by_id(
        db=db,
        user_id=user_id,
    )


def require_current_user(
    request: Request,
    db: DbSession,
) -> User:
    user = get_current_user(
        request=request,
        db=db,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다.",
        )

    return user