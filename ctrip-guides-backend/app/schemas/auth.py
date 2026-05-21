"""Auth schemas — register, login, token."""
from __future__ import annotations

import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_e164: Optional[str] = Field(default=None, pattern=r"^\+[1-9]\d{6,14}$")
    password: str = Field(min_length=10, max_length=128)
    role: UserRole
    locale: str = "en-US"
    display_name: str = Field(min_length=1, max_length=80)


class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_e164: Optional[str] = None
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class CurrentUser(BaseModel):
    id: uuid.UUID
    role: UserRole
    email: Optional[str] = None
