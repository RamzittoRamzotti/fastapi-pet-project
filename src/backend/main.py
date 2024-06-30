import os.path
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from jwt_utils.demo_jwt_auth import router
from books_utils.books import books_router

app = FastAPI()
app.mount("/images", StaticFiles(directory=Path(__file__).parent.parent / "frontend" / "public" / "images"),
          name="images")
app.include_router(router)
app.include_router(books_router)
origins = [
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost"
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
