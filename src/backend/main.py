import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from starlette.middleware.cors import CORSMiddleware

from src.backend.jwt_utils.demo_jwt_auth import router, http_bearer

app = FastAPI()

app.include_router(router)

origins = [
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:5005",
    "http://localhost:5000",
    "http://localhost:5010",
    "http://127.0.0.1:5000"

]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def read_root():
    return {"Hello": "World"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5005)
