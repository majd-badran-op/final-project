from app.domain.shared.base_entity import BaseEntity
from dataclasses import dataclass, field


@dataclass
class Member(BaseEntity):
    name: str
    email: str
    id: int | None = field(default=None)
