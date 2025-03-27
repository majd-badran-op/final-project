from .base_repo import BaseRepo
from app.domain.entities.member_entity import Member
from app.infrastructure.database.schema import members
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select


class MembersRepo(BaseRepo[Member]):
    def __init__(self) -> None:
        super().__init__(Member, members)

    async def check_email(self, email: str, session: AsyncConnection) -> bool:
        sql = select(self.table).where(self.table.c.email == email)
        result = await session.execute(sql)
        row = result.scalars().first()
        return row is None
