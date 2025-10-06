"""Database session factory and migration helpers."""

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def get_engine() -> Engine:
    """Return a cached SQLAlchemy engine configured from settings."""
    
    global _engine
    settings = get_settings()
    if _engine is None or str(_engine.url) != settings.database_url:
        connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
        _engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
    return _engine


def get_sessionmaker() -> sessionmaker:
    """Return a cached session factory bound to the current engine."""

    global _SessionLocal
    engine = get_engine()
    if _SessionLocal is None or _SessionLocal.kw.get("bind") is not engine:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
    return _SessionLocal

def _get_alembic_config() -> Config:
    """Build an Alembic configuration bound to the active database URL."""

    settings = get_settings()
    project_root = Path(__file__).resolve().parents[2]
    alembic_cfg = Config(str(project_root / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    alembic_cfg.set_main_option(
        "script_location", str((Path(__file__).resolve().parent / "migrations").resolve())
    )
    return alembic_cfg


def init_db() -> None:
    """Apply the latest database migrations using Alembic."""

    command.upgrade(_get_alembic_config(), "head")


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