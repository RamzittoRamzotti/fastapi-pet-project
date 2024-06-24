from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.backend.config import settings

engine = create_async_engine(url=settings.db.DB_url, echo=True)
