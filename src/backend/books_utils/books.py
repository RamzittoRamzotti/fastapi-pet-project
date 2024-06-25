from fastapi import Query, HTTPException
from starlette import status

from src.backend.books_utils.crud import get_all_books

from fastapi import APIRouter

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
