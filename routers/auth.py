
from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from database import get_db
from model import User,RefreshToken
from schemas import UserCreate, UserResponse,UserLogin,ChangePassword
from security import create_access_token, verify_access_token, get_current_admin

from fastapi import Depends
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone


from security import (
    create_access_token,
    verify_access_token,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
password_hash = PasswordHash.recommended()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    new_user = User(
        email=user_data.email,
        hashed_password=password_hash.hash(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not password_hash.verify(
        user_data.password,
        existing_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


   
    access_token = create_access_token(
        user_id=existing_user.id,
        role=existing_user.role,
    )

    refresh_token = create_refresh_token(
        user_id=existing_user.id,
    )

    refresh_token_record = RefreshToken(
        token=refresh_token,
        user_id=existing_user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )

    db.add(refresh_token_record)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/test-token")
def test_token(authorization: str = Header()):
    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token",
        )

    try:
        payload = verify_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {
        "message": "JWT is valid",
        "user_id": payload["sub"],
        "role": payload["role"],
    }

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post("/refresh")
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    try:
        payload = verify_access_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
            )

        user_id = int(payload["sub"])

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )

    token_record = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == refresh_token,
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
        )
        .first()
    )

    if token_record is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token is revoked or not found",
        )

    if token_record.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    new_access_token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


class LogoutRequest(BaseModel):
    refresh_token: str


@router.post("/logout")
def logout(
    data: LogoutRequest,
    db: Session = Depends(get_db),
):
    token_record = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == data.refresh_token,
            RefreshToken.revoked == False,
        )
        .first()
    )

    if token_record is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token is invalid or already revoked",
        )

    token_record.revoked = True
    db.commit()

    return {"message": "Logged out successfully"}


@router.post("/change-password")
def change_password(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify the current password
    if not password_hash.verify(
        data.current_password,
        current_user.hashed_password,
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect",
        )

    # Prevent reusing the same password
    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different",
        )

    # Hash and save the new password
    current_user.hashed_password = password_hash.hash(
        data.new_password
    )

    # Revoke the user's existing refresh tokens
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
        RefreshToken.revoked.is_(False),
    ).update(
        {RefreshToken.revoked: True},
        synchronize_session=False,
    )

    db.commit()

    return {"message": "Password changed successfully"}
