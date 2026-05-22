"""JWT + password hashing utilities."""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings


def hash_password(password: str) -> str:
    """Hash password using SHA-256 + salt (no C dependency)."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against stored hash."""
    try:
        salt, stored_hash = hashed.split("$", 1)
        return hashlib.sha256(f"{salt}{plain}".encode()).hexdigest() == stored_hash
    except ValueError:
        return False


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
