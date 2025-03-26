from .base_repo import BaseRepo
from app.domain.entities.book_entity import Book
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, join
from app.infrastructure.database.schema import books, members


class BooksRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(Book, books)

    async def get_all_books_for_member(self, member_id: str, session: Session) -> List[Book] | None:
        j = join(books, members, books.c.borrowed_by == members.c.id)
        query = select(
            books.c.id, books.c.title, books.c.author, books.c.is_borrowed,
            books.c.borrowed_date, books.c.borrowed_by, members.c.name
        ).select_from(j).where(books.c.borrowed_by == member_id)
        result = session.execute(query).fetchall()
        if result:
            books_list = [
                Book(
                    id=row.id,
                    title=row.title,
                    author=row.author,
                    is_borrowed=row.is_borrowed,
                    borrowed_date=row.borrowed_date,
                    borrowed_by=row.borrowed_by,
                    member_name=row.name
                )
                for row in result
            ]
            return books_list
        return None
