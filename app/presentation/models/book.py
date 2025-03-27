from datetime import datetime
from .shared import DataModel
from typing import Optional
import uuid


class BookRequest(DataModel):
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_date: Optional[datetime] = None
    borrowed_by: Optional[uuid.UUID] = None


class BookResponse(DataModel):
    title: str | None
    author: str | None
    id: int | None
    is_borrowed: bool | None
    borrowed_date: datetime | None
    borrowed_by: uuid.UUID | None
    message: Optional[str] = None
