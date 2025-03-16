from flask import jsonify, Response, make_response
from flask.views import MethodView
from app.application.services.books_services import BooksServices


class BorrowView(MethodView):
    def __init__(self) -> None:
        self.books_service = BooksServices()

    def post(self, book_id: str, member_id: str) -> Response:
        book, message, status_code = self.books_service.borrow(book_id, member_id)
        return make_response(jsonify({'code': status_code, 'message': message, 'book': book.__dict__}))
