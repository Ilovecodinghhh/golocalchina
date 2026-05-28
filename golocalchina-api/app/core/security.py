"""Argon2 password hashing + PyJWT token issuance / verification.

Merged from golocalchina-backend's security module:
- Argon2id for password hashing (OWASP recommended, replaces SHA-256+salt)
- PyJWT for JWT (replaces unmaintained python-jose)
"""
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
    """Hash password using Argon2id."""
    return _hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against Argon2 hash."""
    try:
        _hasher.verify(hashed, plain)
        return True
    except VerifyMismatchError:
        return False


TokenType = Literal["access", "refresh"]


def create_access_token(subject: str, role: str) -> str:
    """Create a JWT access token."""
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str) -> str:
    """Create a JWT refresh token."""
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=settings.jwt_refresh_token_expire_days)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT token."""
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
