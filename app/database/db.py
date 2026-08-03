import asyncio
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(get_settings().database_url, pool_pre_ping=True)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session:
        yield session


async def init_db(retries: int = 5) -> None:
    from app.database.models import ContactRequest, User  # noqa: F401

    for attempt in range(retries):
        try:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            return
        except Exception:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2**attempt)
