from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio

from config import DBSettings

engine = create_async_engine(url=DBSettings.DB_url, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def check_db():
    async with engine.begin() as connection:
        res = await connection.execute(text("SELECT VERSION()"))
        print(f'{res=}')


asyncio.run(check_db())
