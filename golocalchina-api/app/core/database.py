"""Async SQLAlchemy engine + session factory. Supports SQLite and PostgreSQL."""
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

db_url = settings.database_url
_is_sqlite = "sqlite" in db_url

# Ensure SQLite directory exists
if _is_sqlite:
    db_path = db_url.split("///")[-1]
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

connect_args = {}
if _is_sqlite:
    connect_args = {"check_same_thread": False}

# Use pool_pre_ping for PostgreSQL to handle dropped connections
engine_kwargs = {
    "echo": False,
    "connect_args": connect_args,
}
if not _is_sqlite:
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = 5
    engine_kwargs["max_overflow"] = 10

engine = create_async_engine(db_url, **engine_kwargs)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables():
    """Create all tables — used on startup."""
    from app.models.base import Base
    from app.models import user, listing, booking  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db_type = "PostgreSQL" if not _is_sqlite else "SQLite"
    print(f"[DB] Tables created. Type: {db_type}")
