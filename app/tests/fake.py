from factory import Factory, Faker
from app.domain.entities.book_entity import Book
from app.domain.entities.member_entity import Member


class BookFactory(Factory):
    class Meta:
        model = Book
    id = None
    title = Faker('sentence')
    author = Faker('name')


class MemberFactory(Factory):
    class Meta:
        model = Member
    id = None
    name = Faker('name')
    email = Faker('email')
