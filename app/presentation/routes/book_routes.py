from fastapi import APIRouter
from app.presentation.view.books_view import BookView
from app.domain.entities.book_entity import Book
from typing import Dict

book_router = APIRouter()
book_view = BookView()


@book_router.get('/')
async def get_books() -> Dict:
    return await book_view.get_all_books()


@book_router.get('/{book_id}')
async def get_book_by_id(book_id: str) -> Dict:
    return await book_view.get_book_by_id(book_id)


@book_router.post('/')
async def add_book(book: Book) -> Dict:
    return await book_view.post(book)


@book_router.patch('/{book_id}')
async def update_book(book_id: str, book: dict) -> Dict:
    return await book_view.patch(book_id, book)


@book_router.delete('/{book_id}')
async def delete_book(book_id: str) -> Dict:
    return await book_view.delete(book_id)


@book_router.post('/borrow/{book_id}/{member_id}')
async def borrow(book_id: str, member_id: str) -> Dict:
    return await book_view.borrow_book(book_id, member_id)


@book_router.post('/return/{book_id}')
async def return_book(book_id: str) -> Dict:
    return await book_view.return_book(book_id)
