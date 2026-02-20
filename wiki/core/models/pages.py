from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import Uuid, Integer, String

from wiki.core.database import db

category_pivot_table = db.Table(
    "category_page",
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
    Column("page_id", Integer, ForeignKey("pages.id"), primary_key=True),
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


class Page(db.Model):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    namespace: Mapped[str] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(unique=True)
    redirect_to: Mapped[int] = mapped_column(
        ForeignKey("pages.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    current_version_id: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False)


class Revisions(db.Model):
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
