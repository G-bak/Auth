"""Data access helpers for user persistence."""

from typing import Iterable, Optional

from sqlalchemy.orm import Session

from app.db.models import Role, User


class UserRepository:
    """Encapsulates CRUD operations for users."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def list(self) -> Iterable[User]:
        return self.session.query(User).all()

    def create(
        self,
        *,
        email: str,
        hashed_password: str,
        full_name: str | None = None,
        roles: Iterable[Role] | None = None,
    ) -> User:
        user = User(email=email, hashed_password=hashed_password, full_name=full_name)
        if roles:
            user.roles.extend(roles)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def add_role(self, user: User, role: Role) -> User:
        if role not in user.roles:
            user.roles.append(role)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
        return user