import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from . import utils as auth_utils
from src.backend.config import settings
from src.backend.models import User
from sqlalchemy import select

engine = create_async_engine(url=settings.db.DB_url, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
john = User(
    username='john',
    password=auth_utils.hash_password('qwerty'),
    email='john@mail.ru',
)
sam = User(
    username='sam',
    password=auth_utils.hash_password('password'),
)


async def initial_inserts():
    async with async_session() as session:
        async with session.begin():
            session.add_all([john, sam])
            await session.commit()


async def get_user_from_db_by_username(username: str):
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.username == username)
            username_ = await session.execute(query)
            result = username_.scalar_one_or_none()
            return result


async def get_user_from_db_by_email(email: str):
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.email == email)
            email_ = await session.execute(query)
            result = email_.scalar_one_or_none()
            return result
# asyncio.run(initial_inserts())
