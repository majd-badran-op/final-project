from pydantic import BaseModel
from datetime import datetime
import uuid


class Book(BaseModel):
    id: int | None = None
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_date: datetime | None = None
    borrowed_by: uuid.UUID | None = None

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'is_borrowed': self.is_borrowed,
            'borrowed_date': self.borrowed_date.isoformat() if self.borrowed_date else None,
            'borrowed_by': str(self.borrowed_by) if self.borrowed_by else None
        }

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
