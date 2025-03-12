from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .base_entity import BaseEntity


@dataclass
class Book(BaseEntity):
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_date: Optional[datetime] = None
    borrowed_by: Optional[int] = None

    def borrow(self, member: int):
        self.is_borrowed = True
        self.borrowed_date = datetime.now()
        self.borrowed_by = member

    def return_book(self):
        self.is_borrowed = False
        self.borrowed_date = None
        self.borrowed_by = None

    def copy_from(self, other: 'Book') -> None:
        self.title = other.title
        self.author = other.author
        self.is_borrowed = other.is_borrowed
        self.borrowed_date = other.borrowed_date
        self.borrowed_by = other.borrowed_by
