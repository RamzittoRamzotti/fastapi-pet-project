import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from schemas import UserSchema
from . import utils as auth_utils
from src.backend.config import settings
from src.backend.models import User
from sqlalchemy import select, insert

from .validation import get_current_active_auth_user

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


async def insert_new_user(user: User):
    async with async_session() as session:
        async with session.begin():
            query = insert(User).values(username=user.username, email=user.email, password=user.password)
            await session.execute(query)
            await session.commit()


# asyncio.run(initial_inserts())

async def is_admin(user: UserSchema = Depends(get_current_active_auth_user)):
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.username == user.username)
            await session.execute(query)
            result = await session.scalar_one_or_none()
            if result.is_admin:
                return result
