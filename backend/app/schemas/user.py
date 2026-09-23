from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

Username = Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, pattern=r"^[a-z0-9_.-]{3,50}$")]
Password = Annotated[str, StringConstraints(min_length=8, max_length=128)]


class LoginIn(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, max_length=50)]
    password: Annotated[str, StringConstraints(max_length=128)]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    is_admin: bool
    is_active: bool


class UserCreate(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    username: Username
    password: Password
    is_admin: bool = False


class UserUpdate(BaseModel):
    is_active: bool | None = None
    is_admin: bool | None = None
    password: Password | None = None


class ChangePasswordIn(BaseModel):
    current_password: str
    new_password: Password
