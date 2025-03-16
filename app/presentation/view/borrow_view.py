from flask import jsonify, Response, make_response
from flask.views import MethodView
from app.application.services.members_services import MembersServices


class BorrowView(MethodView):
    def __init__(self) -> None:
        self.member_service = MembersServices()

    def post(self, book_id: str, member_id: str) -> Response:
        book, message, status_code = self.member_service.borrow(book_id, member_id)
        return make_response(jsonify({'code': status_code, 'message': message, 'book': book.__dict__}))
