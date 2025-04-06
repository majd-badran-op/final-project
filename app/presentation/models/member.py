from .shared import DataModel
from typing import Any
import uuid


class MemberRequest(DataModel):
    name: str
    email: str


class MemberResponse(DataModel):
    id: uuid.UUID | None
    name: str | None
    email: str | None
    books: list[dict[str, Any]] | str | None = []
    message: str | None = None
