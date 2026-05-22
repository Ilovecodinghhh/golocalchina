"""Common FastAPI dependencies: auth, current user, role guards."""
from __future__ import annotations

import uuid
from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole, UserStatus


class AuthError(HTTPException):
    def __init__(self, detail: str = "invalid_token") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise AuthError("missing_bearer")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError as e:
        raise AuthError("expired_token") from e
    except jwt.InvalidTokenError as e:
        raise AuthError("invalid_token") from e
    if payload.get("type") != "access":
        raise AuthError("wrong_token_type")
    try:
        user_id = uuid.UUID(payload["sub"])
    except (KeyError, ValueError) as e:
        raise AuthError("malformed_subject") from e
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None or user.status != UserStatus.active:
        raise AuthError("user_inactive")
    return user


def require_role(*roles: UserRole):
    async def _guard(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="forbidden_role")
        return user
    return _guard


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "")


def get_locale(request: Request) -> str:
    return getattr(request.state, "locale", "en-US")
