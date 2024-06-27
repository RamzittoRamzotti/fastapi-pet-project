import shutil

from fastapi import Query, HTTPException, Form, UploadFile, File, Path
from sqlalchemy import null
from starlette import status
from typing_extensions import Annotated
from src.backend.models import Book
from src.backend.books_utils.crud import (get_all_books,
                                          add_book_db,
                                          get_book_by_id,
                                          delete_book_db,
                                          search_book_db, update_book_db)

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


@books_router.get("/{book_id}")
async def get_book(
        book_id: int
):
    book = await get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No book found by this id."
        )
    return {'book': book}


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


@books_router.delete("/{book_id}")
async def delete_book(book_id: int):
    result = await delete_book_db(book_id=book_id)
    if result:
        return status.HTTP_200_SUCCESS
    else:
        HTTPException(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Couldnt delete the book"
        )


@books_router.patch("/update_book/{book_id}")
async def update_book(
        book_id: int = Path(),
        title: str | None = Form(default=None),
        author: str | None = Form(default=None),
        desc: str | None = Form(default=None),
        img: UploadFile | None = File(default=None),
        user_id: int | None = Form(default=None)):
    old_book = await get_book_by_id(book_id)
    print(old_book)
    if not old_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if title is not None:
        old_book.title = title
    if author is not None:
        old_book.author = author
    if desc is not None:
        old_book.desc = desc
    if img:
        with open(f'src/frontend/public/images/{img.filename}', "wb+") as file:
            shutil.copyfileobj(img.file, file)
        image_filename = img.filename
        old_book.title_picture = image_filename
    if user_id is not None:
        old_book.user_id = user_id
    updated_book = await update_book_db(old_book)
    return {"result": updated_book}


@books_router.get("/search")
async def search_book(text: Annotated[str | None, Query()] = None):
    books = await search_book_db(text)
    return {'books': books}
