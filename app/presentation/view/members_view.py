from fastapi.responses import JSONResponse
from app.domain.entities.member_entity import Member
from app.application.services.members_services import MembersServices


class MemberView:
    def __init__(self) -> None:
        self.members_service = MembersServices()

    async def get_all_members(self) -> JSONResponse:
        members, status_code = self.members_service.get_all()
        return JSONResponse(
            content={
                'code': status_code,
                'members': [member.to_dict() for member in members]
            },
            status_code=status_code
        )

    async def get_member_by_id(self, member_id: str) -> JSONResponse:
        member, status_code = self.members_service.get_by_id(member_id)
        return JSONResponse(
            content={
                'code': status_code,
                'member': member.to_dict()
            },
            status_code=status_code
        )

    async def add_member(self, member: Member) -> JSONResponse:
        member, status_code = self.members_service.add(member)
        return JSONResponse(
            content={
                'code': status_code,
                'member': member.to_dict()
            },
            status_code=status_code
        )

    async def update_member(self, member_id: str, member: Member) -> JSONResponse:
        member_data = {
            'id': member_id,
            'name': member.name,
            'email': member.email,
        }
        message, status_code = self.members_service.update(member_id, member_data)
        return JSONResponse(
            content={
                'code': status_code,
                'message': message
            },
            status_code=status_code
        )

    async def delete_member(self, member_id: str) -> JSONResponse:
        message, status_code = self.members_service.delete(member_id)
        return JSONResponse(
            content={
                'code': status_code,
                'message': message
            },
            status_code=status_code
        )
