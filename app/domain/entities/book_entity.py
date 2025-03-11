from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from member_entity import Member
from base_entity import BaseEntity


@dataclass
class Book(BaseEntity):
    id: Optional[int] = None
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_date: Optional[datetime] = None
    borrowed_by: Optional['Member'] = None

    def borrow(self, member: 'Member'):
        ''' Method to borrow this book '''
        self.is_borrowed = True
        self.borrowed_date = datetime.now()
        self.borrowed_by = member
        member.borrowed_books.append(self)

    def return_book(self):
        ''' Method to return the book '''
        self.is_borrowed = False
        self.borrowed_date = None
        self.borrowed_by = None

    def __str__(self):
        return f'Book(id={self.id}, title={self.title}, author={self.author})'
