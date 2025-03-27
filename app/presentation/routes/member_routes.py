from fastapi import APIRouter
from app.application.services.members_services import MembersServices
from app.application.services.books_services import BooksServices
from app.presentation.models.member import MemberRequest, MemberResponse
from app.domain.entities.member_entity import Member
from app.domain.entities.book_entity import Book
import uuid
member_router = APIRouter()
member_view = MembersServices()
book_serves = BooksServices()


@member_router.get('/')
async def get_members() -> list[MemberResponse]:
    members = await member_view.get_all()
    print(f"Received data: {members}")
    return [MemberResponse(**Member.to_dict(member)) for member in members]


@member_router.get('/{member_id}')
async def get_member_by_id(member_id: uuid.UUID) -> MemberResponse:
    member = await member_view.get_by_id(member_id)
    return MemberResponse(**Member.to_dict(member))


@member_router.post('/')
async def add_member(member: MemberRequest) -> MemberResponse:
    new_member = Member(**vars(member))
    saved_member = await member_view.add(new_member)
    return MemberResponse(**Member.to_dict(saved_member))


@member_router.patch('/{member_id}')
async def update_member(member_id: uuid.UUID, member: MemberRequest) -> MemberResponse:
    updated_member, result = await member_view.update(member_id, Member.from_dict(Member.to_dict(member)))
    return MemberResponse(**Member.to_dict(updated_member), message=result)


@member_router.delete('/{member_id}')
async def delete_member(member_id: uuid.UUID) -> MemberResponse:
    deleted_member, result = await member_view.delete(member_id)
    return MemberResponse(**Member.to_dict(deleted_member), message=result)


@member_router.post('/books/{member_id}')
async def member_books(member_id: uuid.UUID) -> MemberResponse:
    member = await member_view.get_by_id(member_id)
    books = await book_serves.get_all_books_for_member(member_id)

    return MemberResponse(
        id=member.id,
        name=member.name,
        email=member.email,
        books=[Book.to_dict(book) for book in books] if books else []
    )
