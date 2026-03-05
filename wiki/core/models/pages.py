from datetime import datetime
from typing import TYPE_CHECKING, Any, List
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Uuid

from wiki.core.database import db

if TYPE_CHECKING:
    from wiki.core.models.authentication import User

category_pivot_table = db.Table(
    "category_page",
    Column(
        "category_id",
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    ),
    Column(
        "page_id",
        Integer,
        ForeignKey("pages.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
)

interlinks_table = db.Table(
    "interlinks",
    Column("likes_from_id", Integer, ForeignKey("categories.id"), primary_key=True),
    Column("links_to_title", String, primary_key=True),
)


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    parent_category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", onupdate="CASCADE", ondelete="SET NULL")
    )

    pages: Mapped[List["Page"]] = relationship(
        secondary=category_pivot_table, back_populates="categories"
    )


class Page(db.Model):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    namespace: Mapped[str] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(unique=True)
    redirect_to: Mapped[int] = mapped_column(
        ForeignKey("pages.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    current_version_id: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False)

    revisions: Mapped[List["Revision"]] = relationship(back_populates="page")

    categories: Mapped[List[Category]] = relationship(
        secondary=category_pivot_table, back_populates="pages"
    )


class Revision(db.Model):
    __tablename__ = "revisions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    page_id: Mapped[int] = mapped_column(
        ForeignKey("pages.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False
    )
    created_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    constructed_hash: Mapped[str] = mapped_column()
    parent_hash: Mapped[str] = mapped_column()
    parent_id: Mapped[UUID] = mapped_column(
        ForeignKey("revisions.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    base_content: Mapped[bytes] = mapped_column()
    delta: Mapped[bytes] = mapped_column()
    draft: Mapped[bool] = mapped_column(default=True)
    imported: Mapped[bool] = mapped_column(default=False)
    size: Mapped[int] = mapped_column(default=0)
    change: Mapped[int] = mapped_column(default=0)

    page: Mapped[Page] = relationship(back_populates="revisions")
    user: Mapped["User"] = relationship(back_populates="revisions")


class Metadata(db.Model):
    __tablename__ = "metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_type: Mapped[str] = mapped_column()
    parent_id: Mapped[int] = mapped_column()
    group: Mapped[str] = mapped_column(index=True, nullable=True)
    key: Mapped[str] = mapped_column(index=True, nullable=False)
    value: Mapped[bytes] = mapped_column(nullable=False)
    cast_to: Mapped[str] = mapped_column(nullable=False, default="string")

    def get_value(self):
        if self.cast_to == "str":
            return str(self.value, "utf-8")

        if self.cast_to == "int":
            return int.from_bytes(self.value)

        return self.value

    def set_value(self, value: Any):
        if type(value) == int:
            self.value = int.to_bytes(value)
            self.cast_to = "int"
            return

        if type(value) == str:
            self.value = value.encode("utf-8")
            self.cast_to = "str"
            return

        self.value = value
        self.cast_to = "bytes"


class Change(db.Model):
    __tablename__ = "changes"

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column()
    completed_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    object_type: Mapped[str] = mapped_column()
    object_id: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="changes")
