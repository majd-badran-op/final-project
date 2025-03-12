from .base_repo import BaseRepo
from app.domain.entities.book_entity import Book
from app.infrastructure.database.schema import books


class BooksRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(Book, books)
