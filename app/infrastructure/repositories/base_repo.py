from typing import Generic, TypeVar, Type, List, Any
from app.domain.entities.base_entity import BaseEntity
from sqlalchemy import Table, insert, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.engine import CursorResult

E = TypeVar('E', bound=BaseEntity)


class BaseRepo(Generic[E]):
    def __init__(self, entity: Type[E], table: Table) -> None:
        self.entity = entity
        self.table = table

    def insert(self, entity: E, session: Session) -> E | None:
        data = {key: value for key, value in vars(entity).items() if key != 'id'}
        sql = insert(self.table).values(**data).returning(*self.table.columns)
        result = session.execute(sql)
        inserted_row = result.fetchone()
        return self.entity(**inserted_row._mapping) if inserted_row else None

    def get_all(self, session: Session) -> List[E]:
        sql = select(self.table)
        result = session.execute(sql)
        entities = [self.entity(**row._mapping) for row in result.fetchall()]
        return entities

    def get(self, id: str, session: Session) -> E | None:
        sql = select(self.table).where(self.table.c.id == id)
        result = session.execute(sql).fetchone()
        return self.entity(**result._mapping) if result else None

    def update(self, entity: dict[str, Any], id: str, session: Session) -> bool:
        data = {key: value for key, value in entity.items() if key != 'id'}
        sql = update(self.table).where(self.table.c.id == id).values(**data)
        result: CursorResult[Any] = session.execute(sql)
        return result.rowcount > 0

    def delete(self, id: str, session: Session) -> bool:
        sql = delete(self.table).where(self.table.c.id == id)
        result: CursorResult[Any] = session.execute(sql)
        return result.rowcount > 0
