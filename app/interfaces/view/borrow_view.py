from flask import jsonify, Response
from flask.views import MethodView
from app.application.services.books_services import BooksServices


class BorrowView(MethodView):
    def __init__(self) -> None:
        self.books_service = BooksServices()

    def post(self, book_id: int, member_id: int) -> Response:
        book, message, status_code = self.books_service.borrow(book_id, member_id)
        return jsonify({'message': message, 'book': book.__dict__}), status_code
