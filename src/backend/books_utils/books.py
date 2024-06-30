import shutil
import sys

from fastapi import Query, HTTPException, Form, UploadFile, File, Path
from starlette import status
from typing_extensions import Optional
from books_utils.crud import (get_all_books,
                              add_book_db,
                              get_book_by_id,
                              delete_book_db,
                              search_book_db, update_book_db)

from fastapi import APIRouter
from internal.schemas import BookSchema
from internal.tasks import send_mail

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
    filename = img.filename
    if filename.endswith(".jpeg"):
        filename.replace(".jpeg", ".jpg")
    with open(f'src/frontend/public/images/{filename}', "wb+") as file:
        shutil.copyfileobj(img.file, file)
    book = BookSchema(
        title=title,
        author=author,
        description=desc,
        title_picture=filename,
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
        return status.HTTP_200_OK
    else:
        HTTPException(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Couldnt delete the book"
        )


@books_router.patch("/update_book/{book_id}")
async def update_book(
        book_id: str = Path(),
        title: str | None = Form(default=None),
        author: str | None = Form(default=None),
        desc: str | None = Form(default=None),
        img: UploadFile | None = File(default=None)):
    old_book = await get_book_by_id(int(book_id))
    if not old_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if title is not None:
        old_book.title = title
    if author is not None:
        old_book.author = author
    if desc is not None:
        old_book.desc = desc
    if img:
        filesname = img.filename
        if filesname.endswith(".jpeg"):
            filesname.replace(".jpeg", ".jpg")
        with open(f'src/frontend/public/images/{filesname}', "wb+") as file:
            shutil.copyfileobj(img.file, file)
        old_book.title_picture = filesname
    updated_book = await update_book_db(old_book)
    return {"result": updated_book}


@books_router.get("/search/")
async def search_book(text: Optional[str] = Query(default=None, min_length=1)):
    print(text)
    books = await search_book_db(text)
    return {'books': books}


@books_router.patch("/reserve_book/{book_id}")
async def reserve_book(
        book_id: int,
        email: str = Form(),
        user_id: int = Form()):
    old_book = await get_book_by_id(book_id)
    old_book.user_id = user_id
    updated_book = await update_book_db(old_book)
    book_schema = BookSchema(**old_book.as_dict())
    send_mail.delay(email, book_schema)
    return {"result": updated_book}
