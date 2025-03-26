from app.presentation.models.book import BookRequest, BookResponse
from app.application.services.books_services import BooksServices
from app.domain.entities.book_entity import Book
from fastapi import APIRouter

book_router = APIRouter()
book_view = BooksServices()


@book_router.get('/')
async def get_books() -> list[BookResponse]:
    books = await book_view.get_all()
    return [BookResponse(**Book.to_dict(book)) for book in books]


@book_router.get('/{book_id}')
async def get_book_by_id(book_id: str) -> BookResponse:
    book = await book_view.get_by_id(book_id)
    return BookResponse(**Book.to_dict(book))


@book_router.post('/')
async def add_book(book: BookRequest) -> BookResponse:
    book_dict = book.model_dump()
    new_book = Book.from_dict(book_dict)
    saved_book = await book_view.add(new_book)
    return BookResponse(**Book.to_dict(saved_book))


@book_router.patch('/{book_id}')
async def update_book(book_id: str, book: BookRequest) -> BookResponse:
    book = await book_view.update(book)
    return BookResponse(**Book.to_dict(book))


@book_router.delete('/{book_id}')
async def delete_book(book_id: str) -> BookResponse:
    book = await book_view.delete(book_id)
    return BookResponse(**Book.to_dict(book))


@book_router.post('/borrow/{book_id}/{member_id}')
async def borrow(book_id: str, member_id: str) -> BookResponse:
    book = await book_view.borrow(book_id)
    return BookResponse(**Book.to_dict(book))


@book_router.post('/return/{book_id}')
async def return_book(book_id: str) -> BookResponse:
    return await book_view.return_book(book_id)
