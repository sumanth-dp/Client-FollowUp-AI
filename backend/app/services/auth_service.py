from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.app.core.security import hash_password
from backend.app.models.user import User
from backend.app.schemas.auth import UserCreate

from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.scalar(
        select(User).where(
            or_(
                User.username == user_data.username,
                User.email == user_data.email,
            )
        )
    )

    if existing_user:
        raise ValueError("Username or email already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    username: str,
    password: str,
):
    user = db.scalar(
        select(User).where(User.username == username)
    )

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(
    db: Session,
    username: str,
    password: str,
):
    user = authenticate_user(db, username, password)

    if not user:
        return None

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return access_token