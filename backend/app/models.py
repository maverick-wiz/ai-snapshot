"""
SQLAlchemy 2.0 Async ORM Models
AISNP-24 · Owner: ATLAS
"""
import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    Boolean, String, Text, SmallInteger, CHAR,
    ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMPTZ
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMPTZ, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMPTZ, default=utcnow, onupdate=utcnow)

    preferences: Mapped[Optional["UserPreference"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    sessions: Mapped[list["UserSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    default_country: Mapped[str] = mapped_column(CHAR(2), default="US")
    watchlist_tickers: Mapped[list] = mapped_column(JSONB, default=lambda: ["NVDA", "AMD", "TSM", "ASML", "MSFT", "AVGO"])
    refresh_interval_secs: Mapped[int] = mapped_column(SmallInteger, default=5)
    news_limit: Mapped[int] = mapped_column(SmallInteger, default=20)
    theme: Mapped[str] = mapped_column(String(16), default="dark")
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMPTZ, default=utcnow, onupdate=utcnow)

    user: Mapped["User"] = relationship(back_populates="preferences")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_token: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMPTZ, default=utcnow)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMPTZ, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(TIMESTAMPTZ, default=utcnow)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="sessions")


class AppConfig(Base):
    __tablename__ = "app_config"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    config_key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    config_value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMPTZ, default=utcnow, onupdate=utcnow)
