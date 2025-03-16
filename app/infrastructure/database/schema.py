from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import UUID
import uuid

metadata = MetaData()

members = Table(
    'members', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False, unique=True)
)

books = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('author', String, nullable=False),
    Column('is_borrowed', Boolean, default=False),
    Column('borrowed_date', DateTime, nullable=True),
    Column('borrowed_by', UUID(as_uuid=True), ForeignKey('members.id', ondelete="SET NULL"), nullable=True)
)
