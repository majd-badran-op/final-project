from fastapi import APIRouter
from app.presentation.view.members_view import MemberView
from app.domain.entities.member_entity import Member
from typing import Dict

member_router = APIRouter()
member_view = MemberView()


@member_router.get('/')
async def get_members() -> Dict:
    return await member_view.get_all_members()


@member_router.get('/{member_id}')
async def get_member_by_id(member_id: str) -> Dict:
    return await member_view.get_member_by_id(member_id)


@member_router.post('/')
async def add_member(member: Member) -> Dict:
    return await member_view.add_member(member)


@member_router.patch('/{member_id}')
async def update_member(member_id: str, member: Member) -> Dict:
    return await member_view.update_member(member_id, member)


@member_router.delete('/{member_id}')
async def delete_member(member_id: str) -> Dict:
    return await member_view.delete_member(member_id)
