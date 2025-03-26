from typing import Type, TypeVar
from pydantic import BaseModel
from app.domain.shared.base_entity import BaseEntity


R = TypeVar('R', bound='DataModel')
E = TypeVar('E', bound=BaseEntity)


class DataModel(BaseModel):
    @classmethod
    def from_entity(cls: Type[R], entity: E, exclude: list[str] | None = None) -> R:
        return cls(**entity.to_dict(exclude))

    @classmethod
    def from_entity_list(cls: Type[R], entities: list[E], exclude: list[str] | None = None) -> list[R]:
        return [cls.from_entity(entity, exclude) for entity in entities]
