from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from wiki.core.database import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=False)
    source: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    is_authenticated = True
    is_anonymous = False

    @property
    def is_active(self) -> bool:
        return self.email is not None and self.active

    def get_id(self) -> str:
        return str(self.username)
