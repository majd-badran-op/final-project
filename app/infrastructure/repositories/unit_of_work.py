from typing import Optional, Type
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from app.infrastructure.database.con import engine


class UnitOfWork:
    def __init__(self) -> None:
        self.engine: AsyncEngine = engine
        self.connection: AsyncConnection

    async def __aenter__(self) -> 'UnitOfWork':
        self.connection = await self.engine.connect()
        await self.connection.begin()
        return self

    async def commit(self) -> None:
        if self.connection:
            await self.connection.commit()

    async def rollback(self) -> None:
        if self.connection:
            await self.connection.rollback()

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException], traceback: Optional[Type[BaseException]]) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        if self.connection:
            await self.connection.close()
