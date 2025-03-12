from app.infrastructure.repositories.books_repo import BooksRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.book_entity import Book
from .members_services import MembersServices


class BooksServices:
    def __init__(self) -> None:
        self.repo = BooksRepo()
        self.member_serves = MembersServices()

    def add(self, entity: Book) -> tuple[Book, int]:
        with UnitOfWork(self.repo) as uow:
            uow.repo.insert(entity, uow.session)
        return entity, 200

    def borrow(self, book_id: int, member_id: int) -> tuple[Book, dict, int]:
        with UnitOfWork(self.repo) as uow:
            book: Book = uow.repo.get(book_id, uow.session)
            member, message, status_code = self.member_serves.get_by_id(member_id)

            if not book:
                raise ValueError('No books found')
            elif not member:
                raise ValueError('Member Not found')
            elif book.is_borrowed:
                raise ValueError('Book is already borrowed')

            book.borrow(member.id)
            uow.repo.update(book, book_id, uow.session)
        return book, {'message': f'{book.title} borrowed successfully by {member.name}'}, 200

    def get_all(self) -> tuple[list[Book], int] | dict:
        with UnitOfWork(self.repo) as uow:
            books = uow.repo.get_all(uow.session)
        if not books:
            raise ValueError('No books found')
        return books, 200

    def get_by_id(self, id: int) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            book_entity = uow.repo.get(id, uow.session)
        if book_entity is None:
            raise ValueError('Book not found')
        return book_entity, 200

    def update(self, id: int, entity: Book) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            book_entity: Book = uow.repo.get(id, uow.session)
            if book_entity is None:
                raise ValueError('Book not found')
            book_entity.copy_from(entity)
            uow.repo.update(book_entity, id, uow.session)
        return {'message': 'Book updated successfully'}, 200

    def delete(self, id: int) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            book_to_delete = uow.repo.get(id, uow.session)
            if not book_to_delete:
                raise ValueError('Book not found')
            result = uow.repo.delete(id, uow.session)
            if not result:
                raise ValueError('Failed to delete book')
        return {'message': 'Book deleted successfully'}, 200

    def return_book(self, book_id: int) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            book: Book = uow.repo.get(book_id, uow.session)
            if not book:
                raise ValueError('No books found')
            elif not book.is_borrowed:
                raise ValueError('Book is already not borrowed')

            book.return_book()
            uow.repo.update(book, book_id, uow.session)
        return book, {'message': f'book with title {book.title} is now available for borrowing.'}, 200
