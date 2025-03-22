from pydantic import BaseModel
import uuid


class Member(BaseModel):
    id: uuid.UUID | None = None
    name: str
    email: str

    def to_dict(self):
        return {
            'id': str(self.id) if self.id else None,
            'name': self.name,
            'email': self.email
        }
