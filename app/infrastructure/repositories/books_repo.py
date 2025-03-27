from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncConnection
from app.domain.entities.book_entity import Book
from sqlalchemy.sql import select
from app.infrastructure.database.schema import books
import uuid


class BooksRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(Book, books)

    async def get_all_books_for_member(self, member_id: uuid.UUID, session: AsyncConnection) -> list[Book]:
        query = select(books).where(books.c.borrowed_by == member_id)
        result = await session.execute(query)
        rows = result.fetchall()
        return [Book(**row._mapping) for row in rows] if rows else []
