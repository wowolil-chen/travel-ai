from sqlalchemy.orm import Session

from app.core.security import (
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    """用户业务"""

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            password_hash=get_password_hash(user_data.password),
            nickname=user_data.nickname,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate(
        db: Session,
        username: str,
        password: str,
    ) -> User | None:

        user = UserService.get_by_username(
            db=db,
            username=username,
        )

        if user is None:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user