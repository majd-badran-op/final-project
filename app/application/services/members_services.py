from app.infrastructure.repositories.members_repo import MembersRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.member_entity import Member
from app.domain.exceptions.member_exceptions import (
    MemberNotFoundError,
    EmailAlreadyExistsError
)
from typing import Any
import uuid


class MembersServices:
    def __init__(self) -> None:
        self.repo = MembersRepo()

    async def add(self, entity: Member) -> Member:
        async with UnitOfWork() as uow:
            check_email: bool = await self.repo.check_email(entity.email, uow.connection)
            if not check_email:
                raise EmailAlreadyExistsError('The email address already exists.')
            member_entity = await self.repo.insert(entity, uow.connection)
            if member_entity is None:
                raise ValueError('Failed to insert member.')
            return member_entity

    async def get_all(self) -> list[Member]:
        async with UnitOfWork() as uow:
            members = await self.repo.get_all(uow.connection)
            if not members:
                return []
        return members

    async def get_by_id(self, id: uuid.UUID) -> Member | None:
        async with UnitOfWork() as uow:
            member_entity = await self.repo.get(id, uow.connection)
            if member_entity is None:
                raise MemberNotFoundError()
        return member_entity

    async def update(self, id: uuid.UUID, entity: dict[str, Any]) -> tuple[Member, str]:
        cleaned_entity: dict = {}
        async with UnitOfWork() as uow:
            member = await self.get_by_id(id)
            if not member:
                raise MemberNotFoundError()

            for key, value in entity.items():
                if value is not None:
                    cleaned_entity[key] = value

            updated_member = await self.repo.update(cleaned_entity, id, uow.connection)
        return updated_member, 'Member updated successfully'

    async def delete(self, id: uuid.UUID) -> tuple[Member, str]:
        async with UnitOfWork() as uow:
            member = await self.get_by_id(id)
            if not member:
                raise MemberNotFoundError()
            deleted = await self.repo.delete(id, uow.connection)
        if deleted:
            return member, 'Member deleted successfully'
        else:
            return member, 'Can\'t delete Member'
