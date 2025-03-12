from flask import abort, jsonify, Response
from flask.views import MethodView
from app.application.services.books_services import BooksServices


class ReturnView(MethodView):
    def __init__(self) -> None:
        self.books_service = BooksServices()

    def post(self, book_id: int) -> Response:
        try:
            book, message, status_code = self.books_service.return_book(book_id)
            return jsonify({'message': message, 'book': book.__dict__}), status_code
        except ValueError as e:
            abort(400, description=str(e))
