from flask import abort, jsonify, request, Response
from flask.views import MethodView
from app.application.services.books_services import BooksServices
from app.domain.entities.book_entity import Book


class BookView(MethodView):
    def __init__(self) -> None:
        self.books_service = BooksServices()

    def get(self, book_id: int = None) -> Response:
        if book_id is None:
            try:
                books, status_code = self.books_service.get_all()
                return jsonify([book.__dict__ for book in books]), status_code
            except ValueError as e:
                abort(404, description=str(e))
        else:
            try:
                book, status_code = self.books_service.get_by_id(book_id)
                return jsonify(book.__dict__), status_code
            except ValueError as e:
                abort(404, description=str(e))

    def post(self) -> Response:
        data = request.get_json()
        if not data:
            abort(400, description='No input data provided')

        try:
            entity = Book(
                id=None,
                title=data.get('title'),
                author=data.get('author'),
            )
            entity, status_code = self.books_service.add(entity)
            return jsonify(entity.__dict__), status_code
        except ValueError as e:
            abort(400, description=str(e))

    def put(self, book_id: int) -> Response:
        data = request.get_json()
        if not data:
            abort(400, description='No input data provided')

        try:
            entity = Book(
                id=None,
                title=data.get('title'),
                author=data.get('author'),
            )
            message, status_code = self.books_service.update(book_id, entity)
            return jsonify(message), status_code
        except ValueError as e:
            abort(404, description=str(e))

    def delete(self, book_id: int) -> Response:
        try:
            message, status_code = self.books_service.delete(book_id)
            return jsonify(message), status_code
        except ValueError as e:
            abort(404, description=str(e))

    def post_borrow(self, book_id: int, member_id: int) -> Response:
        try:
            book, message, status_code = self.books_service.borrow(book_id, member_id)
            return jsonify({'message': message, 'book': book.__dict__}), status_code
        except ValueError as e:
            abort(400, description=str(e))
