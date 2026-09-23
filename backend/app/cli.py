"""Create the first admin user:  uv run python -m app.cli create-admin <username> "<Full Name>"
The password is asked interactively (never passed on the command line / shell history)."""

import getpass
import sys

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models import User


def create_admin(username: str, name: str, password: str) -> None:
    with SessionLocal() as db:
        if db.scalar(select(User).where(User.username == username.lower())):
            sys.exit(f"User '{username}' already exists")
        db.add(User(name=name, username=username.lower(), password_hash=hash_password(password), is_admin=True))
        db.commit()
    print(f"Admin '{username}' created")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] != "create-admin":
        sys.exit(__doc__)
    password = getpass.getpass("Password (min 8 chars): ")
    if len(password) < 8 or password != getpass.getpass("Repeat password: "):
        sys.exit("Passwords must match and be at least 8 characters")
    create_admin(sys.argv[2], sys.argv[3], password)
