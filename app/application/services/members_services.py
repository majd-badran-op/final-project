from app.infrastructure.repositories.members_repo import MembersRepo
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.domain.entities.member_entity import Member
from app.domain.entities.book_entity import Book


class MembersServices:
    def __init__(self) -> None:
        self.repo = MembersRepo()

    def add(self, entity: Member) -> tuple[Member, int]:
        with UnitOfWork(self.repo) as uow:
            member_entity = uow.repo.insert(entity, uow.session)
            return member_entity, 200

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

    def get_member_books(self, id: int) -> tuple[Member, list[Book], int]:
        with UnitOfWork(self.repo) as uow:
            member = uow.repo.get(id, uow.session)
            if not member:
                raise ValueError('Member not found')
            member_books = self.repo.get_all_books_for_member(id, uow.session)
        if not member_books:
            raise ValueError('Member dont have any books')
        return member_books, member, 200
