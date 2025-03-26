from app.infrastructure.repositories.members_repo import MembersRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.member_entity import Member
from app.domain.exceptions.member_exceptions import (
    MemberNotFoundError,
    FailedToDeleteMemberError,
    EmailAlreadyExistsError
)
from typing import Any


class MembersServices:
    def __init__(self) -> None:
        self.repo = MembersRepo()

    async def add(self, entity: Member) -> tuple[Member, int]:
        with UnitOfWork() as uow:
            check_email: bool = self.repo.check_email(entity.email, uow.session)
            if check_email:
                if (member_entity := self.repo.insert(entity, uow.session)):
                    return member_entity, 200
            else:
                raise EmailAlreadyExistsError('The email address already exists.')

    async def get_all(self) -> tuple[list[Member] | str, int]:
        with UnitOfWork() as uow:
            if not (members := self.repo.get_all(uow.session)):
                return 'No members found', 200
            return members, 200

    async def get_by_id(self, id: str) -> tuple[Member, int]:
        with UnitOfWork() as uow:
            if not (member_entity := self.repo.get(id, uow.session)):
                raise MemberNotFoundError()
        return member_entity, 200

    async def update(self, id: str, entity: dict[str, Any]) -> tuple[dict[str, Any], int]:
        cleaned_entity: dict = {}
        with UnitOfWork() as uow:
            if not (self.get_by_id(id)[0]):
                raise MemberNotFoundError()
            for key, value in entity.items():
                if value is not None:
                    cleaned_entity[key] = value
            self.repo.update(cleaned_entity, id, uow.session)
        return {'message': 'Member updated successfully'}, 200

    async def delete(self, id: str) -> tuple[dict[str, str], int]:
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
