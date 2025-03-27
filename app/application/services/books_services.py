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
import uuid


class BooksServices:
    def __init__(self) -> None:
        self.repo = BooksRepo()
        self.member_services = MembersServices()

    async def add(self, entity: Book) -> Book:
        async with UnitOfWork() as uow:
            book_entity = await self.repo.insert(entity, uow.connection)
            return book_entity

    async def get_all(self) -> list[Book]:
        async with UnitOfWork() as uow:
            books = await self.repo.get_all(uow.connection)
            if not books:
                return 'No books found'
        return books

    async def get_all_books_for_member(self, id: uuid.UUID) -> list[Book] | str:
        async with UnitOfWork() as uow:
            books = await self.repo.get_all_books_for_member(id, uow.connection)
        return books if books else 'No books available.'

    async def get_by_id(self, id: int) -> Book | None:
        async with UnitOfWork() as uow:
            book_entity = await self.repo.get(id, uow.connection)
            if book_entity is None:
                raise BookNotFoundError()
        return book_entity

    async def update(self, id: int, entity: dict[str, Any]) -> tuple[Book, str]:
        cleaned_entity: dict = {}
        async with UnitOfWork() as uow:
            book = await self.get_by_id(id)
            if not book:
                raise BookNotFoundError()

            for key, value in entity.items():
                if value is not None:
                    cleaned_entity[key] = value

            updated_book = await self.repo.update(cleaned_entity, id, uow.connection)
        return updated_book, 'Book updated successfully'

    async def delete(self, id: int) -> tuple[Book, str]:
        async with UnitOfWork() as uow:
            book = await self.get_by_id(id)
            if not book:
                raise BookNotFoundError()
            deleted = await self.repo.delete(id, uow.connection)
            if not deleted:
                raise FailedToDeleteBookError()
        return book, 'Book deleted successfully'

    async def borrow(self, book_id: int, member_id: str) -> tuple[Book, str]:
        book = await self.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(f'Book with id {book_id} not found.')
        if book.is_borrowed:
            raise BookAlreadyBorrowedError(f'The book {book.title} is already borrowed.')
        member = await self.member_services.get_by_id(member_id)
        if not member or not member.id:
            raise MemberNotFoundError(f'Member with id {member_id} not found.')
        book.borrow(member_id)
        await self.update(book_id, vars(book))
        return book, f'{book.title} borrowed successfully by {member.name}'

    async def return_book(self, book_id: int) -> tuple[Book | None, str]:
        updated_entity: dict = {}
        async with UnitOfWork() as uow:
            book = await self.get_by_id(book_id)
            if not book:
                raise BookNotFoundError('Book not found for return.')
            if not book.is_borrowed:
                raise BookReturnError()
            book.return_book()
            for key, value in vars(book).items():
                updated_entity[key] = value
            await self.repo.update(updated_entity, book_id, uow.connection)
        return book, f'Book with title \'{book.title}\' is now available for borrowing.'
