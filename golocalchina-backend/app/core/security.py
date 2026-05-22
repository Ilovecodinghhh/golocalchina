"""Argon2 password hashing + JWT issuance / verification."""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings

_hasher = PasswordHasher()  # OWASP defaults: t=3, m=64MiB, p=4


def hash_password(plain: str) -> str:
    return _hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        _hasher.verify(hashed, plain)
        return True
    except VerifyMismatchError:
        return False


TokenType = Literal["access", "refresh"]


def create_token(
    *, subject: str | uuid.UUID, token_type: TokenType, role: str
) -> str:
    now = datetime.now(timezone.utc)
    if token_type == "access":
        exp = now + timedelta(minutes=settings.jwt_access_minutes)
    else:
        exp = now + timedelta(days=settings.jwt_refresh_days)

    payload: dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
