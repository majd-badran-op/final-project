from typing import Generic, TypeVar, Type, List, Any
from app.domain.shared.base_entity import BaseEntity
from sqlalchemy import Table, insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine.result import Result, Row
import uuid

E = TypeVar("E", bound=BaseEntity)


class BaseRepo(Generic[E]):
    def __init__(self, entity: Type[E], table: Table) -> None:
        self.entity = entity
        self.table = table

    async def insert(self, entity: E, conn: AsyncConnection) -> E:
        data = {key: value for key, value in vars(entity).items() if key != "id"}
        sql = insert(self.table).values(**data).returning(*self.table.columns)
        result: Result = await conn.execute(sql)
        inserted_row: Row | None = result.fetchone()
        if inserted_row is None:
            raise ValueError('Insert failed: no row returned.')
        return self.entity(**inserted_row._mapping)

    async def get_all(self, conn: AsyncConnection) -> List[E]:
        sql = select(self.table)
        result: Result = await conn.execute(sql)
        rows: List[Row] = list(result.fetchall())
        return [self.entity(**row._mapping) for row in rows]

    async def get(self, id: uuid.UUID | int, conn: AsyncConnection) -> E | None:
        sql = select(self.table).where(self.table.c.id == id)
        result: Result = await conn.execute(sql)
        row: Row | None = result.fetchone()
        return self.entity(**row._mapping) if row else None

    async def update(self, entity: dict[str, Any], id: uuid.UUID | int, conn: AsyncConnection) -> E:
        data = {key: value for key, value in entity.items() if key != "id"}
        sql = update(self.table).where(self.table.c.id == id).values(**data).returning(*self.table.columns)
        result: Result = await conn.execute(sql)
        row: Row | None = result.fetchone()
        if row is None:
            raise ValueError("Update failed: no row returned.")
        return self.entity(**row._mapping)

    async def delete(self, id: uuid.UUID | int, conn: AsyncConnection) -> bool:
        sql = delete(self.table).where(self.table.c.id == id)
        result = await conn.execute(sql)
        try:
            return result.rowcount > 0
        except AttributeError:
            return False
