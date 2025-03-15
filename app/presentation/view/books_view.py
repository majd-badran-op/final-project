from typing import Optional
from flask import jsonify, request, Response, make_response
from flask.views import MethodView
from app.application.services.books_services import BooksServices
from app.domain.entities.book_entity import Book


class BookView(MethodView):
    def __init__(self) -> None:
        self.books_service = BooksServices()

    def get(self, book_id: Optional[int] = None) -> Response:
        if book_id is None:
            books, status_code = self.books_service.get_all()
            return make_response(jsonify({'code': status_code, 'books': books}))
        else:
            book, status_code = self.books_service.get_by_id(book_id)
            return make_response(jsonify({'code': status_code, 'book': book}))

    def post(self) -> Response:
        data = request.get_json()
        book = Book(
            id=None,
            title=data.get('title'),
            author=data.get('author'),
        )
        book, status_code = self.books_service.add(book)
        return make_response(jsonify({'code': status_code, 'books': book}))

    def put(self, book_id: int) -> Response:
        data = request.get_json()
        entity = Book(
            id=None,
            title=data.get('title'),
            author=data.get('author'),
        )
        message, status_code = self.books_service.update(book_id, entity)
        return make_response(jsonify({'code': status_code, 'message': message}))

    def delete(self, book_id: int) -> Response:
        message, status_code = self.books_service.delete(book_id)
        return make_response(jsonify({'code': status_code, 'message': message}))
