from .base_repo import BaseRepo
from app.domain.entities.member_entity import Member
from app.infrastructure.database.schema import members
from sqlalchemy.orm import Session
from sqlalchemy import select


class MembersRepo(BaseRepo[Member]):
    def __init__(self) -> None:
        super().__init__(Member, members)

    def check_email(self, email: str, session: Session) -> bool:
        sql = select(self.table).where(self.table.c.email == email)
        result = session.execute(sql).fetchone()
        if not result:
            return True
        return False
