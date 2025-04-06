from fastapi import APIRouter, HTTPException
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
    return [MemberResponse(**member.to_dict()) for member in members]


@member_router.get('/{member_id}')
async def get_member_by_id(member_id: uuid.UUID) -> MemberResponse:
    member = await member_view.get_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberResponse(**member.to_dict())


@member_router.post('/')
async def add_member(member: MemberRequest) -> MemberResponse:
    new_member = Member(**vars(member))
    saved_member = await member_view.add(new_member)
    return MemberResponse(**saved_member.to_dict())


@member_router.patch('/{member_id}')
async def update_member(member_id: uuid.UUID, member: MemberRequest) -> MemberResponse:
    updated_member, result = await member_view.update(
        member_id,
        member.to_dict() if hasattr(member, "to_dict") else vars(member)
    )
    if not updated_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberResponse(**updated_member.to_dict(), message=result)


@member_router.delete('/{member_id}')
async def delete_member(member_id: uuid.UUID) -> MemberResponse:
    deleted_member, result = await member_view.delete(member_id)
    if not deleted_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberResponse(**deleted_member.to_dict(), message=result)


@member_router.post('/books/{member_id}')
async def member_books(member_id: uuid.UUID) -> MemberResponse:
    member = await member_view.get_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    books = await book_serves.get_all_books_for_member(member_id)
    books_list = [book.to_dict() for book in books if isinstance(book, Book)]

    return MemberResponse(
        id=member.id if isinstance(member.id, uuid.UUID) else uuid.UUID(str(member.id)),
        name=member.name,
        email=member.email,
        books=books_list
    )
