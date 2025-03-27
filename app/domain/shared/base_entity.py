from typing import Any, Type, TypeVar, Optional
from dataclasses import dataclass, fields, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID
import uuid

T = TypeVar('T', bound='BaseEntityBase')


def datetime_to_iso_str(date: datetime | None) -> str | None:
    if date is None:
        return None
    return date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def get_field_value(field_type: type[Any] | str | Any, field_data: Any) -> Any:
    if field_data is None:
        return None
    if isinstance(field_type, type) and issubclass(field_type, BaseEntityBase):
        return field_type.from_dict(field_data)


def get_attr_value(attr_val: Any, map_primitive: bool = True) -> Any:
    if attr_val is None:
        return None

    if isinstance(attr_val, BaseEntityBase):
        return attr_val.to_dict()

    if isinstance(attr_val, list):
        return [get_attr_value(item) for item in attr_val]

    if not map_primitive:
        return attr_val

    if isinstance(attr_val, UUID):
        return str(attr_val)

    if isinstance(attr_val, datetime):
        return datetime_to_iso_str(attr_val)

    if isinstance(attr_val, Enum):
        return attr_val.value

    return attr_val


@dataclass
class BaseEntityBase:
    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any], exclude: list[str] | None = None) -> T:
        """
        Convert a dictionary to an instance of the class.
        Recursively handles nested data classes and lists of data classes.
        """
        excluded_fields = list(cls.config.from_dict_excluded_fields)
        if exclude:
            excluded_fields = excluded_fields + exclude

        instance_data = {}
        entity_fields = {f.name: f.type for f in fields(cls)}
        for field_name, field_type in entity_fields.items():
            field_data = None
            if field_name not in excluded_fields:
                field_data = data.get(field_name, None)
            instance_data[field_name] = get_field_value(field_type, field_data)

        return cls(**instance_data)

    def to_dict(self, exclude: list[str] | None = None, map_primitive: bool = True) -> dict[str, Any]:
        """Convert the current object to a dictionary and handle nested dataclasses."""
        excluded_fields = list(self.config.to_dict_excluded_fields)
        if exclude:
            excluded_fields = excluded_fields + exclude

        data: dict[str, Any] = {}
        for cls in self.__class__.mro():
            if not hasattr(cls, '__annotations__'):
                continue
            entity_fields = [f.name for f in fields(cls)]
            for field_name in entity_fields:
                if field_name not in excluded_fields:
                    data[field_name] = get_attr_value(getattr(self, field_name, None), map_primitive)

        return data

    class config:
        db_excluded_fields: list[str] = []
        to_dict_excluded_fields: list[str] = []
        from_dict_excluded_fields: list[str] = []


class BaseEntity(BaseEntityBase):
    id: Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))
