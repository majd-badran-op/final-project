from app.infrastructure.repositories.members_repo import MembersRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.member_entity import Member
from sqlalchemy.exc import IntegrityError


class MembersServices:
    def __init__(self) -> None:
        self.repo = MembersRepo()

    def add(self, entity: Member) -> tuple[Member, dict, int]:
        try:
            with UnitOfWork(self.repo) as uow:
                uow.repo.insert(entity, uow.session)
            return entity, {'message': 'Member added successfully'}, 200
        except IntegrityError as e:
            if 'members_email_key' in str(e.orig):
                raise ValueError('This email is already registered. Please use a different email.')
            raise

    def get_all(self) -> tuple[list[Member], int]:
        with UnitOfWork(self.repo) as uow:
            members = uow.repo.get_all(uow.session)
        if not members:
            raise ValueError('No members found')
        return members, 200

    def get_by_id(self, id: int) -> tuple[Member, dict, int]:
        with UnitOfWork(self.repo) as uow:
            member_entity = uow.repo.get(id, uow.session)
        if not member_entity:
            raise ValueError('Member not found')
        return member_entity, {'message': 'Member found successfully'}, 200

    def update(self, id: int, entity: Member) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            existing_member = uow.repo.get(id, uow.session)
            if not existing_member:
                raise ValueError('Member not found')
            existing_member = entity
            uow.repo.update(existing_member, id, uow.session)
        return {'message': 'Member updated successfully'}, 200

    def delete(self, id: int) -> tuple[dict, int]:
        with UnitOfWork(self.repo) as uow:
            member_to_delete = uow.repo.get(id, uow.session)
            if not member_to_delete:
                raise ValueError('Member not found')
            result = uow.repo.delete(id, uow.session)
            if not result:
                raise ValueError('Failed to delete member')
        return {'message': 'Member deleted successfully'}, 200
