"""Database session factory."""

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.db.models import Base

_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def get_engine() -> Engine:
    global _engine
    settings = get_settings()
    if _engine is None or str(_engine.url) != settings.database_url:
        connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
        _engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
    return _engine


def get_sessionmaker() -> sessionmaker:
    global _SessionLocal
    engine = get_engine()
    if _SessionLocal is None or _SessionLocal.kw.get("bind") is not engine:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
    return _SessionLocal


def init_db() -> None:
    """Create database tables if they do not exist."""

    Base.metadata.create_all(bind=get_engine())


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""

    session_factory = get_sessionmaker()
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:  # pragma: no cover - defensive
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Iterator[Session]:
    """FastAPI dependency that yields a database session."""

    with session_scope() as session:
        yield session