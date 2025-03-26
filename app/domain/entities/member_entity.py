from app.domain.shared.base_entity import BaseEntity
import uuid


class Member(BaseEntity):
    id: uuid.UUID | None = None
    name: str
    email: str

    def to_dict(self):
        return {
            'id': str(self.id) if self.id else None,
            'name': self.name,
            'email': self.email
        }
