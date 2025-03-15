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
            response = make_response(jsonify([book.__dict__ for book in books]), status_code)
            return response
        else:
            book, status_code = self.books_service.get_by_id(book_id)
            response = make_response(jsonify(book.__dict__), status_code)
            return response

    def post(self) -> Response:
        data = request.get_json()
        entity = Book(
            id=None,
            title=data.get('title'),
            author=data.get('author'),
        )
        entity, status_code = self.books_service.add(entity)
        return make_response(jsonify(entity.__dict__), status_code)

    def put(self, book_id: int) -> Response:
        data = request.get_json()
        entity = Book(
            id=None,
            title=data.get('title'),
            author=data.get('author'),
        )
        message, status_code = self.books_service.update(book_id, entity)
        return make_response(jsonify({'message': message}), status_code)

    def delete(self, book_id: int) -> Response:
        message, status_code = self.books_service.delete(book_id)
        return make_response(jsonify({'message': message}), status_code)

    def post_borrow(self, book_id: int, member_id: int) -> Response:
        book, message, status_code = self.books_service.borrow(book_id, member_id)
        return make_response(jsonify({'message': message, 'book': book.__dict__}), status_code)
