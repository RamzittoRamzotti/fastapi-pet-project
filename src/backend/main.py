import uvicorn
from fastapi import FastAPI, HTTPException, Form, UploadFile, Query
from fastapi.openapi.models import Response
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing_extensions import Annotated, Optional

from src.backend.books_utils.books import books_router
from src.backend.books_utils.crud import search_book_db
from src.backend.jwt_utils.validation import is_admin
from src.backend.jwt_utils.demo_jwt_auth import router

app = FastAPI()
app.mount("/images", StaticFiles(directory="../frontend/public/images"), name="images")
app.include_router(router)
app.include_router(books_router)
origins = [
    "http://localhost:3000",
    "http://localhost:5000",
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


@app.get("/is-admin")
async def check_admin():
    admin = await is_admin()
    if admin:
        return admin
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
#  uvicorn src.backend.main:app --port 5000 --reload
