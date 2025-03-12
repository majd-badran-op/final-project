from typing import List
from .base_repo import BaseRepo
from app.domain.entities.member_entity import Member
from app.infrastructure.database.schema import members
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.infrastructure.database.schema import books
from app.domain.entities.book_entity import Book


class MembersRepo(BaseRepo[Member]):
    def __init__(self) -> None:
        super().__init__(Member, members)

    def get_all_books_for_member(self, member_id: int, session: Session) -> List[Book] | None:
        query = select(books.c.title, books.c.author, books.c.id).where(books.c.borrowed_by == member_id)
        result = session.execute(query).fetchall()

        if result:
            return [Book(title=row[0], author=row[1], id=row[2]) for row in result]

        return None
