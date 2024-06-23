from sqlalchemy import String, Column, Integer, LargeBinary, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50), nullable=False)
    email: str = Column(String(255), unique=True, nullable=True)
    password: bytes = Column(LargeBinary(2555), nullable=False)
    active: bool = Column(Boolean(), default=True)
    admin: bool = Column(Boolean(), default=False)

    def __repr__(self):
        return f'User(id={self.id}, name={self.username}, email={self.email})'


class Book(Base):
    __tablename__ = 'books'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(255), nullable=False)
    author: str = Column(String(255), nullable=False)
    title_picture: str = Column(String(255), nullable=False)
    description: str = Column(String(5000), nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'Books(id={self.id}, title={self.title}, author={self.author})'
