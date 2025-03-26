from typing import Optional, Type
from app.infrastructure.database.con import engine
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine


class UnitOfWork:
    def __init__(self) -> None:
        self.session: AsyncEngine = engine
        self.connection: AsyncConnection

    async def __aenter__(self) -> 'UnitOfWork':
        self.connection = await self.engine.connect()
        await self.connection.begin()
        return self

    async def commit(self) -> None:
        if self.session:
            self.session.commit()

    async def rollback(self) -> None:
        if self.session:
            self.session.rollback()

    async def __exit__(self, exc_type: Optional[Type[BaseException]],
                       exc_value: Optional[BaseException], traceback: Optional[Type[BaseException]]) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()
        if self.session:
            self.session.close()
