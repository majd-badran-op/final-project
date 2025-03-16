from typing import Optional, Tuple
from app.infrastructure.repositories.books_repo import BooksRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.book_entity import Book
from app.domain.exceptions.member_exceptions import MemberNotFoundError
from app.domain.exceptions.book_exception import (
    BookNotFoundError,
    BookAlreadyBorrowedError,
    BookReturnError,
    FailedToDeleteBookError
)


class BooksServices:
    def __init__(self) -> None:
        self.repo = BooksRepo()

    @property
    def member_serves(self):
        from .members_services import MembersServices
        return MembersServices()

    def add(self, entity: Book) -> Tuple[Book, int]:
        with UnitOfWork() as uow:
            book_entity = self.repo.insert(entity, uow.session)
            if not book_entity:
                raise BookNotFoundError()
            return book_entity, 200

    def borrow(self, book_id: str, member_id: str) -> tuple[Optional[Book], dict, int]:
        with UnitOfWork() as uow:
            book, code = self.get_by_id(book_id)
            result = self.member_serves.get_by_id(member_id)
            member = result[0]
            if book is None:
                raise BookNotFoundError()
            if book.is_borrowed:
                raise BookAlreadyBorrowedError()
            if member is None or member.id is None:
                raise MemberNotFoundError()

            book.borrow(member.id)
            self.repo.update(book, book_id, uow.session)
        return book, {'message': f'{book.title} borrowed successfully by {member.name}'}, 200

    def get_all(self) -> tuple[list[Book], int]:
        with UnitOfWork() as uow:
            books = self.repo.get_all(uow.session)
        if not books:
            raise BookNotFoundError('No books available.')
        return books, 200

    def get_all_books_for_member(self, id: str) -> tuple[list[Book] | str, int]:
        with UnitOfWork() as uow:
            books = self.repo.get_all_books_for_member(id, uow.session)
        if not books:
            return 'No books available.', 200
        return books, 200

    def get_by_id(self, id: str) -> tuple[Book, int]:
        with UnitOfWork() as uow:
            book_entity: Optional[Book] = self.repo.get(id, uow.session)
        if book_entity is None:
            raise BookNotFoundError()
        return book_entity, 200

    def update(self, id: str, entity: Book) -> tuple[dict, int]:
        with UnitOfWork() as uow:
            book_entity, code = self.get_by_id(id)
            if book_entity is None:
                raise BookNotFoundError()
            book_entity.copy_from(entity)
            self.repo.update(book_entity, id, uow.session)
        return {'message': 'Book updated successfully'}, 200

    def delete(self, id: str) -> tuple[dict, int]:
        with UnitOfWork() as uow:
            book_to_delete, code = self.get_by_id(id)
            if book_to_delete is None:
                raise BookNotFoundError()
            result = self.repo.delete(id, uow.session)
            if not result:
                raise FailedToDeleteBookError()
        return {'message': 'Book deleted successfully'}, 200

    def return_book(self, book_id: str) -> tuple[Optional[Book], dict, int]:
        with UnitOfWork() as uow:
            book, code = self.get_by_id(book_id)
            if book is None:
                raise BookNotFoundError('Book not found for return.')
            if not book.is_borrowed:
                raise BookReturnError()
            book.return_book()
            self.repo.update(book, book_id, uow.session)
        return book, {'message': f'Book with title \'{book.title}\' is now available for borrowing.'}, 200
