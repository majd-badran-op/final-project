from .base_repo import BaseRepo
from app.domain.entities.member_entity import Member
from app.infrastructure.database.schema import members


class MembersRepo(BaseRepo[Member]):
    def __init__(self) -> None:
        super().__init__(Member, members)
