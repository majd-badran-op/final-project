import factory
from app.domain.entities.book_entity import Book
from app.domain.entities.member_entity import Member


class BookFactory(factory.Factory):
    class Meta:
        model = Book
    id = None
    title = factory.Faker('word')
    author = factory.Faker('name')


class MemberFactory(factory.Factory):
    class Meta:
        model = Member
    id = None
    name = factory.Faker('name')
    email = factory.Faker('email')
