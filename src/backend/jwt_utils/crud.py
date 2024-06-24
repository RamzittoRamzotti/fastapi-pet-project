import sys

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.backend.database import engine
from src.backend.schemas import UserSchema
from src.backend.jwt_utils import utils as auth_utils
from src.backend.models import User
from sqlalchemy import select, insert

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

sys.path.append('C:\\Users\\1\\PycharmProjects\\blog_platform\\src\\backend')

john = User(
    username='john',
    password=auth_utils.hash_password('qwerty'),
    email='john@mail.ru',
)
sam = User(
    username='sam',
    password=auth_utils.hash_password('password'),
)


async def initial_inserts_users():
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


# uvicorn src.backend.main:app --port 5000 --reload


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
async def get_admin(user: UserSchema):
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.username == user.username)
            await session.execute(query)
            result = await session.scalar_one_or_none()
            if result.is_admin:
                return result

# asyncio.run(initial_inserts_books())
