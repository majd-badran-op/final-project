from dataclasses import dataclass


@dataclass
class BaseEntity:
    id: str | None
