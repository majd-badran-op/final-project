from app.infrastructure.repositories.members_repo import MembersRepo
from .books_services import BooksServices
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.member_entity import Member
from app.domain.entities.book_entity import Book
from sqlalchemy.exc import IntegrityError
from app.domain.exceptions.member_exceptions import (
    MemberNotFoundError,
    FailedToAddMemberError,
    FailedToDeleteMemberError,
    EmailAlreadyExistsError
)
from app.domain.exceptions.book_exception import (
    BookNotFoundError,
    BookAlreadyBorrowedError
)
from typing import Any


class MembersServices:
    def __init__(self) -> None:
        self.repo = MembersRepo()
        self.book_serves = BooksServices()

    def add(self, entity: Member) -> tuple[Member, int]:
        with UnitOfWork() as uow:
            try:
                if not (member_entity := self.repo.insert(entity, uow.session)):
                    raise FailedToAddMemberError()
                return member_entity, 200

            except IntegrityError as e:
                if 'unique constraint' in str(e.orig):
                    raise EmailAlreadyExistsError('The email address already exists.')
                else:
                    raise e

    def get_all(self) -> tuple[list[Member], int]:
        with UnitOfWork() as uow:
            if not (members := self.repo.get_all(uow.session)):
                raise MemberNotFoundError('No members found')
        return members, 200

    def get_by_id(self, id: str) -> tuple[Member, int]:
        with UnitOfWork() as uow:
            if not (member_entity := self.repo.get(id, uow.session)):
                raise MemberNotFoundError()
        return member_entity, 200

    def update(self, id: str, entity: dict[str, Any]) -> tuple[dict[str, Any], int]:
        cleaned_entity: dict = {}
        with UnitOfWork() as uow:
            if not (self.get_by_id(id)[0]):
                raise MemberNotFoundError()
            for key, value in entity.items():
                if value is not None:
                    cleaned_entity[key] = value
            self.repo.update(cleaned_entity, id, uow.session)
        return {'message': 'Member updated successfully'}, 200

    def delete(self, id: str) -> tuple[dict[str, str], int]:
        with UnitOfWork() as uow:
            if not (self.get_by_id(id)[0]):
                raise MemberNotFoundError()
            elif not isinstance((books := self.book_serves.get_all_books_for_member(id)[0]), str):
                raise ValueError(
                    f'Cannot delete member with ID {id} because they still have {len(books)} '
                    'borrowed books.'
                )

            if not self.repo.delete(id, uow.session):
                raise FailedToDeleteMemberError()
        return {'message': 'Member deleted successfully'}, 200

    def get_member_books(self, id: str) -> tuple[list[dict[str, Any]] | str, int]:
        if not (self.get_by_id(id)[0]):
            raise MemberNotFoundError()

        member_books = self.book_serves.get_all_books_for_member(id)[0]

        if not member_books:
            return member_books, 200
        return member_books, 200

    def borrow(self, book_id: str, member_id: str) -> tuple[Book | None, dict[str, str], int]:
        to_update_entity: dict = {}
        with UnitOfWork():
            if (book := self.book_serves.get_by_id(book_id)[0]) is None:
                raise BookNotFoundError()
            if book.is_borrowed:
                raise BookAlreadyBorrowedError()
            if (member := self.get_by_id(member_id)[0]) is None or member.id is None:
                raise MemberNotFoundError()
            book.borrow(member_id)
            for key, value in vars(book).items():
                to_update_entity[key] = value
            self.book_serves.update(book_id, to_update_entity)
        return book, {'message': f'{book.title} borrowed successfully by {member.name}'}, 200
