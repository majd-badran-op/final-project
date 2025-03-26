from app.application.services.members_services import MembersServices
from app.application.services.books_services import BooksServices
from app.presentation.models.member import MemberRequest, MemberResponse, UpdateMember
from fastapi import APIRouter

member_router = APIRouter()
member_view = MembersServices()
book_serves = BooksServices()


@member_router.get('/')
async def get_members() -> list[MemberResponse]:
    return await member_view.get_all()


@member_router.get('/{member_id}')
async def get_member_by_id(member_id: str) -> MemberResponse:
    return await member_view.get_by_id(member_id)


@member_router.post('/')
async def add_member(member: MemberRequest) -> MemberResponse:
    return await member_view.add(member)


@member_router.patch('/{member_id}')
async def update_member(member_id: str, member: UpdateMember) -> MemberResponse:
    return await member_view.update(member_id, member)


@member_router.delete('/{member_id}')
async def delete_member(member_id: str) -> MemberResponse:
    return await member_view.delete(member_id)


@member_router.post('/books/{member_id}')
async def member_books(member_id: str) -> MemberResponse:
    return await book_serves.get_all_books_for_member(member_id)
