from .base_repo import BaseRepo
from app.domain.entities.book_entity import Book
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, join
from app.infrastructure.database.schema import books, members


class BooksRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(Book, books)

    def get_all_books_for_member(self, member_id: str, session: Session) -> Optional[List[Dict[str, Any]]]:
        j = join(books, members, books.c.borrowed_by == members.c.id)

        query = select(
            books.c.id, books.c.title, books.c.author, books.c.is_borrowed,
            books.c.borrowed_date, books.c.borrowed_by, members.c.name
        ).select_from(j).where(books.c.borrowed_by == member_id)

        result = session.execute(query).fetchall()
        return [dict(row._mapping) for row in result] if result else None
