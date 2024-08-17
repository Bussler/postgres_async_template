import logging
import os
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app import logger
from app.config import CONFIGS

engine = create_async_engine(
    CONFIGS.instance.POSTGRES_CONFIG.get_connection_string(), pool_pre_ping=True, echo=False, future=True
)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yields connection to currently running db.

    Returns:
        AsyncIterator[AsyncSession]: Connection to the db.

    Yields:
        Iterator[AsyncIterator[AsyncSession]]: Connection to the db.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error(f"Error during db transaction: {e}")
            await session.rollback()
            raise
