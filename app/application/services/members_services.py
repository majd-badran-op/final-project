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
    MemberBooksNotFoundError,
    EmailAlreadyExistsError
)


class MembersServices:
    def __init__(self) -> None:
        self.repo = MembersRepo()
        self.book_serves = BooksServices()

    def add(self, entity: Member) -> tuple[Member, int]:
        with UnitOfWork() as uow:
            try:
                member_entity = self.repo.insert(entity, uow.session)
                if not member_entity:
                    raise FailedToAddMemberError()
            except IntegrityError as e:
                if 'unique constraint' in str(e.orig):
                    raise EmailAlreadyExistsError('The email address already exists.')
                else:
                    raise e
        return member_entity, 200

    def get_all(self) -> tuple[list[Member], int]:
        with UnitOfWork() as uow:
            members = self.repo.get_all(uow.session)
        if not members:
            raise MemberNotFoundError('No members found')
        return members, 200

    def get_by_id(self, id: int) -> tuple[Member, int]:
        with UnitOfWork() as uow:
            member_entity: Member | None = self.repo.get(id, uow.session)
        if not member_entity:
            raise MemberNotFoundError()
        return member_entity, 200

    def update(self, id: int, entity: Member) -> tuple[dict, int]:
        with UnitOfWork() as uow:
            existing_member = self.get_by_id(id)
            if not existing_member:
                raise MemberNotFoundError()
            self.repo.update(entity, id, uow.session)
        return {'message': 'Member updated successfully'}, 200

    def delete(self, id: int) -> tuple[dict, int]:
        with UnitOfWork() as uow:
            member_to_delete = self.get_by_id(id)
            if not member_to_delete:
                raise MemberNotFoundError()
            else:
                result = self.book_serves.get_all_books_for_member(id)
                books = result[0]
                if not isinstance(books, str):
                    raise ValueError(f'Cannot delete member with ID {id} because they have books.')
            result = self.repo.delete(id, uow.session)
            if not result:
                raise FailedToDeleteMemberError()
        return {'message': 'Member deleted successfully'}, 200

    def get_member_books(self, id: int) -> tuple[Member, list[Book], int]:
        member: Member | None = self.get_by_id(id)
        if not member:
            raise MemberNotFoundError()
        member_books = self.book_serves.get_all_books_for_member(id)
        if not member_books:
            raise MemberBooksNotFoundError()
        return member, member_books, 200
