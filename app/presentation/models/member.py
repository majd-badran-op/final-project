from app.presentation.models.book import BookResponse
from .shared import DataModel
import uuid


class MemberRequest(DataModel):
    name: str
    email: str


class MemberResponse(DataModel):
    id: uuid.UUID
    name: str
    email: str
    massage: str | None
    books: list[BookResponse] | None


class UpdateMember(DataModel):
    id: uuid.UUID
    name: str | None
    email: str | None
