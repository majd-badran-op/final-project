from typing import Optional, Tuple
from app.infrastructure.repositories.books_repo import BooksRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.book_entity import Book
from .members_services import MembersServices
from app.domain.exceptions.book_exception import (
    BookNotFoundError,
    BookAlreadyBorrowedError,
    MemberNotFoundError,
    BookReturnError,
    FailedToDeleteBookError
)


class BooksServices:
    def __init__(self) -> None:
        self.repo = BooksRepo()
        self.member_serves = MembersServices()

    def add(self, entity: Book) -> Tuple[Book, int]:
        with UnitOfWork(self.repo) as uow:
            book_entity = uow.repo.insert(entity, uow.session)
            if book_entity:
                return book_entity, 200
            else:
                raise BookNotFoundError()

    def borrow(self, book_id: int, member_id: int) -> tuple[Optional[Book], dict, int]:
        with UnitOfWork(self.repo) as uow:
            book: Optional[Book] = uow.repo.get(book_id, uow.session)
            member, message, status_code = self.member_serves.get_by_id(member_id)

            if book is None:
                raise BookNotFoundError()
            if book.is_borrowed:
                raise BookAlreadyBorrowedError()
            if member is None or member.id is None:
                raise MemberNotFoundError()

            book.borrow(member.id)
            uow.repo.update(book, book_id, uow.session)
        return book, {'message': f'{book.title} borrowed successfully by {member.name}'}, 200

    def get_all(self) -> tuple[list[Book], int]:
        with UnitOfWork(self.repo) as uow:
            books = uow.repo.get_all(uow.session)
        if not books:
            raise BookNotFoundError('No books available.')
        return books, 200

    def get_by_id(self, id: int) -> tuple[Optional[dict], int]:
        with UnitOfWork(self.repo) as uow:
            book_entity: Optional[Book] = uow.repo.get(id, uow.session)
        if book_entity is None:
            raise BookNotFoundError()
        return book_entity, 200

    def update(self, id: int, entity: Book) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            book_entity: Optional[Book] = uow.repo.get(id, uow.session)
            if book_entity is None:
                raise BookNotFoundError()
            book_entity.copy_from(entity)
            uow.repo.update(book_entity, id, uow.session)
        return {'message': 'Book updated successfully'}, 200

    def delete(self, id: int) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            book_to_delete: Optional[Book] = uow.repo.get(id, uow.session)
            if book_to_delete is None:
                raise BookNotFoundError()
            result = uow.repo.delete(id, uow.session)
            if not result:
                raise FailedToDeleteBookError()
        return {'message': 'Book deleted successfully'}, 200

    def return_book(self, book_id: int) -> tuple[Optional[Book], dict, int]:
        with UnitOfWork(self.repo) as uow:
            book: Optional[Book] = uow.repo.get(book_id, uow.session)
            if book is None:
                raise BookNotFoundError('Book not found for return.')
            if not book.is_borrowed:
                raise BookReturnError()

            book.return_book()
            uow.repo.update(book, book_id, uow.session)
        return book, {'message': f'Book with title \'{book.title}\' is now available for borrowing.'}, 200
