from app.infrastructure.repositories.books_repo import BooksRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.book_entity import Book
from app.domain.exceptions.book_exception import (
    BookNotFoundError,
    BookReturnError,
    FailedToDeleteBookError,
    BookAlreadyBorrowedError,
)
from app.domain.exceptions.member_exceptions import (
    MemberNotFoundError
)
from .members_services import MembersServices
from typing import Any


class BooksServices:
    def __init__(self) -> None:
        self.repo = BooksRepo()
        self.member_services = MembersServices()

    def add(self, entity: Book) -> tuple[Book, int]:
        with UnitOfWork() as uow:
            book_entity = self.repo.insert(entity, uow.session)
            return book_entity, 200

    def get_all(self) -> tuple[list[Book] | str, int]:
        with UnitOfWork() as uow:
            if not (books := self.repo.get_all(uow.session)):
                return 'No books found', 200
        return books, 200

    def get_all_books_for_member(self, id: str) -> tuple[list[dict[str, Any]], int] | tuple[str, int]:
        with UnitOfWork() as uow:
            books = self.repo.get_all_books_for_member(id, uow.session)
        return (books, 200) if books else ('No books available.', 200)

    def get_by_id(self, id: str) -> tuple[Book, int]:
        with UnitOfWork() as uow:
            if (book_entity := self.repo.get(id, uow.session)) is None:
                raise BookNotFoundError()
        return book_entity, 200

    def update(self, id: str, entity: dict[str, Any]) -> tuple[dict[str, Any], int]:
        cleaned_entity: dict = {}
        with UnitOfWork() as uow:
            if not (self.get_by_id(id)[0]):
                raise BookNotFoundError()
            for key, value in entity.items():
                if value is not None:
                    cleaned_entity[key] = value
            self.repo.update(cleaned_entity, id, uow.session)
        return {'message': 'Book updated successfully'}, 200

    def delete(self, id: str) -> tuple[dict[str, str], int]:
        with UnitOfWork() as uow:
            if (self.get_by_id(id)[0]) is None:
                raise BookNotFoundError()
            if not self.repo.delete(id, uow.session):
                raise FailedToDeleteBookError()
        return {'message': 'Book deleted successfully'}, 200

    def borrow(self, book_id: str, member_id: str) -> tuple[Book | None, dict[str, str], int]:
        to_update_entity: dict = {}
        with UnitOfWork():
            if (book := self.get_by_id(book_id)[0]) is None:
                raise BookNotFoundError()
            if book.is_borrowed:
                raise BookAlreadyBorrowedError()
            if (member := self.member_services.get_by_id(member_id)[0]) is None or member.id is None:
                raise MemberNotFoundError()
            book.borrow(member_id)
            for key, value in vars(book).items():
                to_update_entity[key] = value
            self.update(book_id, to_update_entity)
        return book, {'message': f'{book.title} borrowed successfully by {member.name}'}, 200

    def return_book(self, book_id: str) -> tuple[Book | None, dict[str, str], int]:
        with UnitOfWork() as uow:
            updated_entity: dict = {}
            if (book := self.get_by_id(book_id)[0]) is None:
                raise BookNotFoundError('Book not found for return.')
            if not book.is_borrowed:
                raise BookReturnError()
            book.return_book()
            for key, value in vars(book).items():
                updated_entity[key] = value
            self.repo.update(updated_entity, book_id, uow.session)
        return book, {'message': f'Book with title \'{book.title}\' is now available for borrowing.'}, 200
