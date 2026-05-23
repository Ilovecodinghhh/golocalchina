"""Auth endpoints — register with email verification + anti-robot."""
import random
import time
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.user import User, TouristProfile, GuideProfile
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory store for verification codes (use Redis in production)
_verification_codes: dict[str, dict] = {}


class SendCodeRequest(BaseModel):
    email: str = Field(min_length=5)


class SendCodeResponse(BaseModel):
    message: str
    # In production, don't return the code — send via email
    # For MVP demo, we return it so the frontend can show it
    demo_code: str = ""


class VerifyCodeRequest(BaseModel):
    email: str
    code: str


def validate_password(password: str) -> list[str]:
    """Check password complexity. Returns list of errors."""
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        errors.append("Password must contain at least one special character (!@#$%^&*...)")
    return errors


@router.post("/send-code", response_model=SendCodeResponse)
async def send_verification_code(req: SendCodeRequest, db: AsyncSession = Depends(get_db)):
    """Send a 6-digit verification code to email.
    MVP: Returns code in response (production: send via email service)."""
    # Check if email already registered
    existing = await db.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    # Rate limit: max 1 code per 60 seconds per email
    if req.email in _verification_codes:
        elapsed = time.time() - _verification_codes[req.email]["created"]
        if elapsed < 60:
            raise HTTPException(status_code=429, detail=f"Wait {60 - int(elapsed)} seconds before requesting a new code")

    code = f"{random.randint(100000, 999999)}"
    _verification_codes[req.email] = {"code": code, "created": time.time(), "verified": False}

    # TODO: In production, send email via SendGrid/Mailgun/AWS SES
    # For MVP, return the code in the response
    return SendCodeResponse(
        message=f"Verification code sent to {req.email}",
        demo_code=code,  # Remove this line in production
    )


@router.post("/verify-code")
async def verify_code(req: VerifyCodeRequest):
    """Verify the email code."""
    stored = _verification_codes.get(req.email)
    if not stored:
        raise HTTPException(status_code=400, detail="No code sent to this email. Request a new one.")

    # Code expires after 10 minutes
    if time.time() - stored["created"] > 600:
        del _verification_codes[req.email]
        raise HTTPException(status_code=400, detail="Code expired. Request a new one.")

    if stored["code"] != req.code:
        raise HTTPException(status_code=400, detail="Invalid code")

    stored["verified"] = True
    return {"message": "Email verified", "verified": True}


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check password complexity
    pwd_errors = validate_password(req.password)
    if pwd_errors:
        raise HTTPException(status_code=400, detail="; ".join(pwd_errors))

    # Check email verification
    stored = _verification_codes.get(req.email)
    if not stored or not stored.get("verified"):
        raise HTTPException(status_code=400, detail="Email not verified. Send and verify a code first.")

    # Check existing
    existing = await db.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(email=req.email, password_hash=hash_password(req.password), role=req.role, status="active", locale=req.locale)
    db.add(user)
    await db.flush()

    if user.role == "tourist":
        db.add(TouristProfile(user_id=user.id, display_name=req.display_name, nationality=req.country, preferred_currency=req.preferred_currency or "USD"))
    elif user.role == "guide":
        db.add(GuideProfile(user_id=user.id, legal_name=req.display_name, display_name=req.display_name,
                            guide_license_no="NONE", guide_license_issuer="NOT_CERTIFIED"))

    await db.flush()

    # Clean up verification code
    _verification_codes.pop(req.email, None)

    return TokenResponse(
        access_token=create_access_token(str(user.id), user.role),
        refresh_token=create_refresh_token(str(user.id)),
        role=user.role, user_id=str(user.id),
    )


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if user.status != "active":
        raise HTTPException(status_code=403, detail="Account not active")
    return TokenResponse(
        access_token=create_access_token(str(user.id), user.role),
        refresh_token=create_refresh_token(str(user.id)),
        role=user.role, user_id=str(user.id),
    )
