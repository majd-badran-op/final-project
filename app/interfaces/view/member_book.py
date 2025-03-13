from flask import jsonify, Response, make_response
from flask.views import MethodView
from app.application.services.members_services import MembersServices


class MemberBookView(MethodView):
    def __init__(self) -> None:
        self.books_service = MembersServices()

    def get(self, member_id: int) -> Response:
        member, books, status_code = self.books_service.get_member_books(member_id)
        return make_response(jsonify(member, books), status_code)
