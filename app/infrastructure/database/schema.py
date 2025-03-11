from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey, MetaData

metadata = MetaData()
members = Table(
    'members', metadata,
    Column('id', primary_key=True, autoincrement=True),
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
    Column('borrowed_by', ForeignKey('members.id'), nullable=True)
)
