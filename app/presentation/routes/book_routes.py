from app.presentation.models.book import BookRequest, BookResponse
from app.application.services.books_services import BooksServices
from app.domain.entities.book_entity import Book
from fastapi import APIRouter, HTTPException

book_router = APIRouter()
book_view = BooksServices()


@book_router.get('/')
async def get_books() -> list[BookResponse]:
    books = await book_view.get_all()
    return [BookResponse(**book.to_dict()) for book in books]


@book_router.get('/{book_id}')
async def get_book_by_id(book_id: int) -> BookResponse:
    book = await book_view.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book.to_dict())


@book_router.post('/')
async def add_book(book: BookRequest) -> BookResponse:
    new_book = Book(**vars(book))
    saved_book = await book_view.add(new_book)
    return BookResponse(**saved_book.to_dict())


@book_router.patch('/{book_id}')
async def update_book(book_id: int, book: dict) -> BookResponse:
    updated_book, result = await book_view.update(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**updated_book.to_dict(), message=result)


@book_router.delete('/{book_id}')
async def delete_book(book_id: int) -> BookResponse:
    book, result = await book_view.delete(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book.to_dict(), message=result)


@book_router.post('/borrow/{book_id}/{member_id}')
async def borrow(book_id: int, member_id: str) -> BookResponse:
    book, result = await book_view.borrow(book_id, member_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book.to_dict(), message=result)


@book_router.post('/return/{book_id}')
async def return_book(book_id: int) -> BookResponse:
    book, result = await book_view.return_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book.to_dict(), message=result)
