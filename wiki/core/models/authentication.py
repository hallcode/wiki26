from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from passlib.hash import argon2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wiki.core.database import db

if TYPE_CHECKING:
    from wiki.core.models.pages import Change, Revision


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=False)
    source: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    revisions: Mapped[List["Revision"]] = relationship(back_populates="user")
    changes: Mapped[List["Change"]] = relationship(back_populates="user")

    is_authenticated = True
    is_anonymous = False

    @property
    def is_active(self) -> bool:
        return self.email is not None and self.active

    def get_id(self) -> str:
        return str(self.username)

    def set_password(self, password_raw: str) -> None:
        password_hash = argon2.hash(password_raw)
        self.password_hash = password_hash

    def check_password(self, password_raw: str) -> bool:
        return argon2.verify(password_raw, str(self.password_hash))
