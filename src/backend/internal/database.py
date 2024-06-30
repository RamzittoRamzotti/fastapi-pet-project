from sqlalchemy.ext.asyncio import create_async_engine

from internal.config import settings

engine = create_async_engine(url=settings.db.DB_url, echo=True)
