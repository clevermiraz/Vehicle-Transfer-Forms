from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import select

from app.core.config import settings
from app.core.deps import DB, CurrentUser
from app.core.security import COOKIE_NAME, create_access_token, hash_password, verify_password
from app.models import User
from app.schemas.user import ChangePasswordIn, LoginIn, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=UserOut)
def login(data: LoginIn, response: Response, db: DB):
    user = db.scalar(select(User).where(User.username == data.username))
    if user is None or not user.is_active or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password")
    response.set_cookie(
        COOKIE_NAME,
        create_access_token(user.id),
        max_age=settings.access_token_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(data: ChangePasswordIn, user: CurrentUser, db: DB):
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Current password is wrong")
    user.password_hash = hash_password(data.new_password)
    db.commit()
