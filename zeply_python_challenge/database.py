from typing import Any
from typing import AsyncIterator
from typing import Iterator

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import sessionmaker

from zeply_python_challenge.config import settings


@as_declarative()
class Base:  # noqa: D101
    __name__: str

    # implicitly adding integer primary key for all declared models
    id: Mapped[int] = Column(Integer, primary_key=True)


class TimeTrackMixin:
    """A mixin for time-tracking models."""

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        onupdate=func.now(),
        nullable=True,
    )


def get_sync_engine() -> Any:
    """Return sync engine."""
    try:
        uri = getattr(settings, "SQLALCHEMY_DATABASE_URI")  # noqa: B009
    except AttributeError:
        raise AttributeError(
            "Please set the SQLALCHEMY_DATABASE_URI in app settings"
        )
    return create_engine(
        uri, echo=settings.SQLALCHEMY_ECHO, pool_pre_ping=True
    )


def get_async_engine() -> Any:
    """Return async engine."""
    try:
        uri = getattr(settings, "SQLALCHEMY_ASYNC_DATABASE_URI")  # noqa: B009
    except AttributeError:
        raise AttributeError(
            "Please set the SQLALCHEMY_ASYNC_DATABASE_URI in app settings"
        )
    return create_async_engine(
        uri, echo=settings.SQLALCHEMY_ECHO, pool_pre_ping=True
    )


def async_session_factory() -> Any:
    """Return asynchronous sqlalchemy session factory."""
    return sessionmaker(
        bind=get_async_engine(),
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


def sync_session_factory() -> Any:
    """Return synchronous sqlalchemy session factory."""
    return sessionmaker(
        bind=get_sync_engine(), autocommit=False, autoflush=False
    )


async def create_async_session() -> AsyncIterator[AsyncSession]:
    """Return asynchronous sqlalchemy session."""
    _session = async_session_factory()
    async with _session() as sess:
        yield sess


def create_sync_session() -> Iterator[Session]:
    """Return synchronous sqlalchemy session."""
    _session = sync_session_factory()
    with _session() as sess:
        yield sess
