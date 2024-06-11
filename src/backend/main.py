import uvicorn
from fastapi import FastAPI, APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models import Base, User
from config import settings
from demo.demo_jwt_auth import router

engine = create_async_engine(url=settings.db.DB_url, echo=True)
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()

route = APIRouter()
app.include_router(route)
app.include_router(router)


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#     async with async_session() as session:
#         async with session.begin():
#             session.add(
#                 User(name="admin", email="asd@mail.ru", password="admin")
#             )
#             await session.commit()


@app.get("/api")
async def read_root():
    return {"Hello": "World"}


@app.post("/isauth")
async def isauth():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
