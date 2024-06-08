import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models import Base, User

engine = create_async_engine("postgresql+asyncpg://admin:admin@localhost")
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            session.add(
                User(name="admin", email="asd@mail.ru", password="admin")
            )
            await session.commit()


@app.get("/api")
async def read_root():
    return {"Hello": "World"}


@app.post("/isauth")
async def isauth():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
