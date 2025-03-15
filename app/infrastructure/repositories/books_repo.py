from .base_repo import BaseRepo
from app.domain.entities.book_entity import Book
from app.infrastructure.database.schema import books
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session


class BooksRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(Book, books)

    def get_all_books_for_member(self, member_id: int, session: Session) -> List[Book] | None:
        query = select(
            books.c.id, books.c.title, books.c.author, books.c.is_borrowed,
            books.c.borrowed_date, books.c.borrowed_by
        ).where(books.c.borrowed_by == member_id)

        result = session.execute(query).fetchall()

        if result:
            return [Book(id=row[0], title=row[1], author=row[2], is_borrowed=row[3],
                         borrowed_date=row[4], borrowed_by=row[5]) for row in result]

        return None
