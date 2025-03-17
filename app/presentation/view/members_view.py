from typing import Optional
from flask import jsonify, request, Response, make_response
from flask.views import MethodView
from app.domain.entities.member_entity import Member
from app.application.services.members_services import MembersServices


class MemberView(MethodView):
    def __init__(self) -> None:
        self.members_service = MembersServices()

    def get(self, member_id: Optional[str] = None) -> Response:
        if member_id:
            member, status_code = self.members_service.get_by_id(member_id)
            return make_response(jsonify({'code': status_code, 'member': member}))
        else:
            members, status_code = self.members_service.get_all()
            return make_response(jsonify({'code': status_code, 'member': members}))

    def post(self) -> Response:
        data = request.get_json()
        member = Member(
            id=None,
            name=data.get('name'),
            email=data.get('email'),
        )
        member, status_code = self.members_service.add(member)
        return make_response(jsonify({'code': status_code, 'member': member}))

    def patch(self, member_id: str) -> Response:
        data = request.get_json()
        member: dict = {
            "id": None,
            "name": data.get("name"),
            "email": data.get("email"),
        }
        message, status_code = self.members_service.update(member_id, member)
        return make_response(jsonify({'code': status_code, 'message': message}))

    def delete(self, member_id: str) -> Response:
        message, status_code = self.members_service.delete(member_id)
        return make_response(jsonify({'code': status_code, 'message': message}))
