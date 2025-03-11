from dataclasses import dataclass, field
from typing import List
from book_entity import Book
from base_entity import BaseEntity


@dataclass
class Member(BaseEntity):
    name: str
    email: str
    borrowed_books: List[Book] = field(default_factory=list)

    def borrow_book(self, book: Book):
        ''' Method to borrow a book '''
        if book.is_borrowed:
            raise Exception(f'Book "{book.title}" is already borrowed.')
        book.borrow(self)

    def __str__(self):
        return f'Member(id={self.id}, name={self.name}, email={self.email})'
