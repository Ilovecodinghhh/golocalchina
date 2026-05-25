"""JWT + password hashing utilities."""
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

_ph = PasswordHasher()
_bearer_scheme = HTTPBearer(auto_error=False)


# ---------------------------------------------------------------------------
# Password hashing — argon2id (memory-hard, GPU-resistant)
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """Hash a password with argon2id."""
    return _ph.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against an argon2 or legacy SHA-256 hash."""
    # Handle legacy SHA-256 hashes from earlier versions (salt$hex)
    if "$argon2" not in hashed and "$" in hashed:
        try:
            salt, stored_hash = hashed.split("$", 1)
            return hashlib.sha256(f"{salt}{plain}".encode()).hexdigest() == stored_hash
        except ValueError:
            return False
    # Argon2 verification
    try:
        return _ph.verify(hashed, plain)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(hashed: str) -> bool:
    """Check if a hash should be upgraded (legacy SHA-256 or old argon2 params)."""
    if "$argon2" not in hashed:
        return True  # Legacy SHA-256 hash
    return _ph.check_needs_rehash(hashed)


# ---------------------------------------------------------------------------
# JWT creation
# ---------------------------------------------------------------------------

def create_access_token(subject: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    return jwt.encode(
        {"sub": subject, "role": role, "exp": expire, "type": "access"},
        settings.jwt_secret_key, algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_token_expire_days)
    return jwt.encode(
        {"sub": subject, "exp": expire, "type": "refresh"},
        settings.jwt_secret_key, algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


# ---------------------------------------------------------------------------
# FastAPI dependency: extract current user from JWT Bearer token
# ---------------------------------------------------------------------------

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> dict:
    """Decode JWT and return {"user_id": ..., "role": ...}.

    Raises 401 if token is missing or invalid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated — Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(credentials.credentials)
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"user_id": user_id, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_role(required: str, current_user: dict = Depends(get_current_user)) -> dict:
    """Factory-free role check. Use role-specific helpers below."""
    if current_user["role"] != required:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Requires {required} role")
    return current_user


async def get_current_tourist(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency that requires the caller to be a tourist."""
    if current_user["role"] != "tourist":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tourist role required")
    return current_user


async def get_current_guide(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency that requires the caller to be a guide."""
    if current_user["role"] != "guide":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Guide role required")
    return current_user
