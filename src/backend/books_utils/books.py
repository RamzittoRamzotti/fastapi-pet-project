import shutil

from fastapi import Query, HTTPException, Form, UploadFile, File
from sqlalchemy import null
from starlette import status
from typing_extensions import Annotated

from src.backend.books_utils.crud import get_all_books, add_book_db

from fastapi import APIRouter

from src.backend.schemas import BookSchema

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get('')
async def get_books(
        skip: int = Query(default=0, alias="skip"),
        limit: int = Query(default=2, alias="limit")
):
    books = await get_all_books(skip, limit)
    if not books:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No books found."
        )
    return books


@books_router.post("/add_book")
async def add_book(title: str = Form(),
                   author: str = Form(),
                   desc: str = Form(),
                   img: UploadFile = File(...)):
    with open(f'src/frontend/public/images/{img.filename}', "wb+") as file:
        shutil.copyfileobj(img.file, file)
    book = BookSchema(
        title=title,
        author=author,
        description=desc,
        title_picture=img.filename,
    )
    result = await add_book_db(book)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book could not be added."
        )
