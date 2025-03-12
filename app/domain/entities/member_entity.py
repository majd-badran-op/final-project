from dataclasses import dataclass
from .base_entity import BaseEntity


@dataclass
class Member(BaseEntity):
    name: str
    email: str
