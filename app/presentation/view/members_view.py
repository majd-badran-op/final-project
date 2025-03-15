from typing import Optional
from flask import jsonify, request, Response, make_response
from flask.views import MethodView
from app.domain.entities.member_entity import Member
from app.application.services.members_services import MembersServices


class MemberView(MethodView):
    def __init__(self) -> None:
        self.members_service = MembersServices()

    def get(self, member_id: Optional[int] = None) -> Response:
        if member_id:
            member, message, status_code = self.members_service.get_by_id(member_id)
            return make_response(jsonify({'message': message, 'member': member.__dict__}), status_code)
        else:
            members, status_code = self.members_service.get_all()
            return make_response(jsonify([member.__dict__ for member in members]), status_code)

    def post(self) -> Response:
        data = request.get_json()
        entity = Member(
            id=None,
            name=data.get('name'),
            email=data.get('email'),
        )
        entity, status_code = self.members_service.add(entity)
        return make_response(jsonify(entity.__dict__), status_code)

    def put(self, member_id: int) -> Response:
        data = request.get_json()
        entity = Member(
            id=None,
            name=data.get('name'),
            email=data.get('email'),
        )
        message, status_code = self.members_service.update(member_id, entity)
        return make_response(jsonify({'message': message}), status_code)

    def delete(self, member_id: int) -> Response:
        message, status_code = self.members_service.delete(member_id)
        return make_response(jsonify({'message': message}), status_code)
