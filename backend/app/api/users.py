from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.deps import DB, AdminUser
from app.core.security import hash_password
from app.models import User
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def list_users(_: AdminUser, db: DB):
    return db.scalars(select(User).order_by(User.name)).all()


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, _: AdminUser, db: DB):
    if db.scalar(select(User).where(User.username == data.username)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")
    user = User(name=data.name, username=data.username, password_hash=hash_password(data.password), is_admin=data.is_admin)
    db.add(user)
    db.commit()
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, admin: AdminUser, db: DB):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    if user.id == admin.id and (data.is_active is False or data.is_admin is False):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "You cannot disable or demote yourself")
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.is_admin is not None:
        user.is_admin = data.is_admin
    if data.password:
        user.password_hash = hash_password(data.password)
    db.commit()
    return user
