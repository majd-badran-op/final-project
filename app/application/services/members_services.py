from app.infrastructure.repositories.members_repo import MembersRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.member_entity import Member
from app.domain.entities.book_entity import Book
from app.domain.exceptions.member_exceptions import (
    MemberNotFoundError,
    FailedToAddMemberError,
    FailedToDeleteMemberError,
    MemberBooksNotFoundError,
)


class MembersServices:
    def __init__(self) -> None:
        self.repo = MembersRepo()

    def add(self, entity: Member) -> tuple[Member, int]:
        with UnitOfWork(self.repo) as uow:
            member_entity = uow.repo.insert(entity, uow.session)
            if not member_entity:
                raise FailedToAddMemberError()
        return member_entity, 200

    def get_all(self) -> tuple[list[Member], int]:
        with UnitOfWork(self.repo) as uow:
            members = uow.repo.get_all(uow.session)
        if not members:
            raise MemberNotFoundError('No members found')
        return members, 200

    def get_by_id(self, id: int) -> tuple[Member, dict, int]:
        with UnitOfWork(self.repo) as uow:
            member_entity: Member | None = uow.repo.get(id, uow.session)
        if not member_entity:
            raise MemberNotFoundError()
        return member_entity, {'message': 'Member found successfully'}, 200

    def update(self, id: int, entity: Member) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            existing_member: Member | None = uow.repo.get(id, uow.session)
            if not existing_member:
                raise MemberNotFoundError()
            uow.repo.update(entity, id, uow.session)
        return {'message': 'Member updated successfully'}, 200

    def delete(self, id: int) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            member_to_delete, books, code = self.get_member_books(id)
            if not member_to_delete:
                raise MemberNotFoundError()
            if books:
                raise ValueError(f'Cannot delete member with ID {id} because they have books.')
            result = uow.repo.delete(id, uow.session)
            if not result:
                raise FailedToDeleteMemberError()
        return {'message': 'Member deleted successfully'}, 200

    def get_member_books(self, id: int) -> tuple[Member, list[Book], int]:
        with UnitOfWork(self.repo) as uow:
            member: Member | None = uow.repo.get(id, uow.session)
            if not member:
                raise MemberNotFoundError()
            member_books: list[Book] | None = self.repo.get_all_books_for_member(id, uow.session)
        if not member_books:
            raise MemberBooksNotFoundError()
        return member, member_books, 200
