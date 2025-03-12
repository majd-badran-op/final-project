from sqlalchemy.orm import Session
from .base_repo import BaseRepo
from typing import Any, Optional, Type
from app.infrastructure.database.con import get_session


class UnitOfWork:
    def __init__(self, repo_class: BaseRepo[Any]) -> None:
        self.session: Session
        self.repo = repo_class

    def __enter__(self) -> 'UnitOfWork':
        self.session = get_session()
        self.transaction = self.session.begin()
        return self

    def commit(self) -> None:
        if self.session:
            self.session.commit()
        else:
            self.rollback()

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException], traceback: Optional[Type[BaseException]]) -> None:
        if exc_type:
            self.rollback()
        if exc_type is None:
            self.commit()
        if self.session:
            self.session.close()
