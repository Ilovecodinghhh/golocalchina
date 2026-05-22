"""Auth endpoints: register, login, refresh, me.

PIPL:
- Every login/registration emits an audit_log row.
- Consent for base account_processing is recorded at registration.
"""
from __future__ import annotations

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.audit import record_audit
from app.core.database import get_db
from app.core.security import create_token, decode_token, hash_password, verify_password
from app.models.audit import AuditAction
from app.models.consent import ConsentPurpose, ConsentRecord, LawfulBasis
from app.models.user import (
    GuideProfile,
    RequesterProfile,
    User,
    UserRole,
    UserStatus,
)
from app.schemas.auth import LoginRequest, RegisterRequest, TokenPair
from app.schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    body: RegisterRequest, request: Request, db: AsyncSession = Depends(get_db)
) -> User:
    if not (body.email or body.phone_e164):
        raise HTTPException(status_code=422, detail="email_or_phone_required")
    if body.role == UserRole.admin:
        raise HTTPException(status_code=403, detail="admin_register_forbidden")

    existing = (
        await db.execute(
            select(User).where(
                or_(
                    User.email == body.email if body.email else False,
                    User.phone_e164 == body.phone_e164 if body.phone_e164 else False,
                )
            )
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=409, detail="user_already_exists")

    user = User(
        email=body.email,
        phone_e164=body.phone_e164,
        password_hash=hash_password(body.password),
        role=body.role,
        locale=body.locale,
        status=UserStatus.active,  # email verification flow is out of MVP scope
    )
    db.add(user)
    await db.flush()

    if body.role == UserRole.requester:
        db.add(RequesterProfile(user_id=user.id, display_name=body.display_name))
    elif body.role == UserRole.guide:
        # Guide profile is created with stub data; KYC submission is a separate step.
        # We DO NOT activate the guide for listings until KYC is approved.
        db.add(
            GuideProfile(
                user_id=user.id,
                legal_name=body.display_name,
                display_name=body.display_name,
                guide_license_no=f"PENDING-{user.id.hex[:12]}",
                guide_license_issuer="PENDING",
                guide_license_issued_on="2000-01-01",
                guide_license_expires_on="2099-12-31",
                guide_license_scan_url="pending://kyc",
                id_card_last4="0000",
            )
        )

    db.add(
        ConsentRecord(
            user_id=user.id,
            purpose=ConsentPurpose.account_processing,
            policy_version="2026-05-21",
            lawful_basis=LawfulBasis.consent,
            jurisdiction="CN",
            granted_from_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
    )

    await record_audit(
        db,
        action=AuditAction.create,
        resource_type="user",
        resource_id=str(user.id),
        actor_id=user.id,
        actor_ip=request.client.host if request.client else None,
        subject_user_id=user.id,
        purpose="account_creation",
        lawful_basis=LawfulBasis.consent.value,
        request_id=getattr(request.state, "request_id", None),
    )
    return user


@router.post("/login", response_model=TokenPair)
async def login(
    body: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)
) -> TokenPair:
    if not (body.email or body.phone_e164):
        raise HTTPException(status_code=422, detail="email_or_phone_required")
    q = select(User).where(
        or_(
            User.email == body.email if body.email else False,
            User.phone_e164 == body.phone_e164 if body.phone_e164 else False,
        )
    )
    user = (await db.execute(q)).scalar_one_or_none()
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid_credentials")
    if user.status != UserStatus.active:
        raise HTTPException(status_code=403, detail="user_inactive")

    await record_audit(
        db,
        action=AuditAction.login,
        resource_type="session",
        actor_id=user.id,
        actor_ip=request.client.host if request.client else None,
        subject_user_id=user.id,
        purpose="authentication",
        lawful_basis=LawfulBasis.contract.value,
        request_id=getattr(request.state, "request_id", None),
    )

    return TokenPair(
        access_token=create_token(
            subject=user.id, token_type="access", role=user.role.value
        ),
        refresh_token=create_token(
            subject=user.id, token_type="refresh", role=user.role.value
        ),
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(authorization: str | None = None) -> TokenPair:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing_bearer")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="invalid_refresh") from e
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="wrong_token_type")
    return TokenPair(
        access_token=create_token(
            subject=payload["sub"], token_type="access", role=payload["role"]
        ),
        refresh_token=create_token(
            subject=payload["sub"], token_type="refresh", role=payload["role"]
        ),
    )


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)) -> User:
    return user
