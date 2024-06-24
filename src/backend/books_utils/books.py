from fastapi import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.books_utils import books_router
from src.backend.books_utils.crud import get_all_books, async_session


@books_router.get('/')
async def get_books(skip: int = Query(default=0, alias="skip"), limit: int = Query(default=2, alias="limit"),
                    db: AsyncSession = Depends(async_session)):
    books = await get_all_books(skip, limit)
