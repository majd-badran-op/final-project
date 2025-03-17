from sqlalchemy.orm import Session
from typing import Optional, Type
from app.infrastructure.database.con import engine


class UnitOfWork:
    def __init__(self) -> None:
        self.session: Session

    def __enter__(self) -> 'UnitOfWork':
        self.session = Session(engine)
        return self

    def commit(self) -> None:
        if self.session:
            self.session.commit()

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException], traceback: Optional[Type[BaseException]]) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()
        if self.session:
            self.session.close()
