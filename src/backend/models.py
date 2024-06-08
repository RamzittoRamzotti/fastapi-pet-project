from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False)
    email: str = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(255), nullable=False)

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, email={self.email})'
