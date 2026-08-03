from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(2), default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ContactRequest(Base):
    __tablename__ = "contact_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(320))
    service: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
