from datetime import datetime
from dataclasses import dataclass
from app.domain.shared.base_entity import BaseEntity
import uuid


@dataclass
class Book(BaseEntity):
    title: str
    author: str
    is_borrowed: bool = False
    id: int | None = None
    borrowed_date: datetime | None = None
    borrowed_by: uuid.UUID | None = None

    def borrow(self, member: str) -> None:
        self.is_borrowed = True
        self.borrowed_date = datetime.now()
        self.borrowed_by = uuid.UUID(member)

    def return_book(self) -> None:
        self.is_borrowed = False
        self.borrowed_date = None
        self.borrowed_by = None

    def copy_from(self, other: 'Book') -> None:
        self.title = other.title
        self.author = other.author
        self.is_borrowed = other.is_borrowed
        self.borrowed_date = other.borrowed_date
        self.borrowed_by = other.borrowed_by
