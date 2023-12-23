import logging
import os
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

logger = logging.getLogger(__name__)

PG_CONNECTION_STRING = os.environ.get(
    "PG_CONNECTION_STRING",
    "postgresql+asyncpg://postgres:password@localhost:5432/postgres_db",
)

async_engine = create_async_engine(
    PG_CONNECTION_STRING, pool_pre_ping=True, echo=False, future=True
)

# AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False, future=True)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    factory = async_sessionmaker(bind=async_engine, autoflush=False, future=True)
    async with factory() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy Error, rollback: ", e)
            await session.rollback()
            raise
