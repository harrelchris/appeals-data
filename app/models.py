from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Sitemap(Base):
    __tablename__ = "sitemap"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(100))
    updated: Mapped[str] = mapped_column(String(20))
    retrieved: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return self.url


class Decision(Base):
    __tablename__ = "decision"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(100))
    updated: Mapped[str] = mapped_column(String(20))
    retrieved: Mapped[str] = mapped_column(String(20))
    text: Mapped[Optional[str]] = mapped_column(String(10000))

    def __repr__(self) -> str:
        return self.url
