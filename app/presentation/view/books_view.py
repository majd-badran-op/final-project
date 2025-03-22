from app.application.services.books_services import BooksServices
from app.domain.entities.book_entity import Book
from fastapi.responses import JSONResponse


class BookView:
    def __init__(self) -> None:
        self.books_service = BooksServices()

    async def get_all_books(self) -> JSONResponse:
        books, status_code = self.books_service.get_all()
        return JSONResponse(
            content={
                'code': status_code,
                'books': [book.to_dict() if isinstance(book, Book) else book for book in books]
            },
            status_code=status_code
        )

    async def get_book_by_id(self, book_id: str) -> JSONResponse:
        book, status_code = self.books_service.get_by_id(book_id)
        return JSONResponse(
            content={
                'code': status_code,
                'book': book.to_dict()
            },
            status_code=status_code
        )

    async def post(self, book: Book) -> JSONResponse:
        book, status_code = self.books_service.add(book)
        return JSONResponse(
            content={
                'code': status_code,
                'book': book.to_dict()
            },
            status_code=status_code
        )

    async def patch(self, book_id: str, book: Book) -> JSONResponse:
        entity = {
            'id': None,
            'title': book.title,
            'author': book.author,
        }
        message, status_code = self.books_service.update(book_id, entity)
        return JSONResponse(
            content={
                'code': status_code,
                'message': message
            },
            status_code=status_code
        )

    async def delete(self, book_id: str) -> JSONResponse:
        message, status_code = self.books_service.delete(book_id)
        return JSONResponse(
            content={
                'code': status_code,
                'message': message
            },
            status_code=status_code
        )

    async def borrow_book(self, book_id: str, member_id: str) -> JSONResponse:
        message, status_code = self.books_service.borrow(book_id, member_id)
        return JSONResponse(
            content={
                'code': status_code,
                'message': message
            },
            status_code=status_code
        )

    async def return_book(self, book_id: str) -> JSONResponse:
        book, message, status_code = self.books_service.return_book(book_id)
        return JSONResponse(
            content={
                'code': status_code,
                'message': message,
                'book': book.to_dict()
            },
            status_code=status_code
        )
