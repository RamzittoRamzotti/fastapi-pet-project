from sqlalchemy import String, Column, Integer, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50), nullable=False)
    email: str = Column(String(255), unique=True, nullable=True)
    password: bytes = Column(LargeBinary(2555), nullable=False)
    active: bool = True

    def __repr__(self):
        return f'User(id={self.id}, name={self.username}, email={self.email})'
