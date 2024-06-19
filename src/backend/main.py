from fastapi import FastAPI, APIRouter

from src.backend.jwt_utils.demo_jwt_auth import router

app = FastAPI()

app.include_router(router)


@app.get("/api")
async def read_root():
    return {"Hello": "World"}
