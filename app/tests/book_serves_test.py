import pytest
from app.application.services.books_services import BooksServices
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.infrastructure.repositories.books_repo import BooksRepo
from app.domain.entities.book_entity import Book
from app.tests.fake import BookFactory, MemberFactory
from app.infrastructure.repositories.members_repo import MembersRepo


@pytest.fixture
def book_fixture():
    book = BookFactory()
    with UnitOfWork(BooksRepo()) as uow:
        created_book = uow.repo.insert(book, uow.session)
    yield created_book
    with UnitOfWork(BooksRepo()) as uow:
        uow.repo.delete(created_book.id, uow.session)


@pytest.fixture
def member_fixture():
    member = MemberFactory()
    with UnitOfWork(MembersRepo()) as uow:
        created_member = uow.repo.insert(member, uow.session)
    yield created_member
    with UnitOfWork(MembersRepo()) as uow:
        uow.repo.delete(created_member.id, uow.session)


def test_create_book(book_fixture):
    assert book_fixture.title is not None
    assert book_fixture.author is not None


def test_get_book_by_id(book_fixture):
    books_service = BooksServices()
    book, status_code = books_service.get_by_id(book_fixture.id)
    assert status_code == 200
    assert book.id == book_fixture.id
    assert book.title == book_fixture.title


def test_borrow_book(book_fixture, member_fixture):
    books_service = BooksServices()
    book, message, status_code = books_service.borrow(book_fixture.id, member_fixture.id)
    assert status_code == 200
    assert message['message'] == f'{book.title} borrowed successfully by {member_fixture.name}'
    assert book.is_borrowed is True
    assert book.borrowed_by == member_fixture.id
    with UnitOfWork(BooksRepo()) as uow:
        uow.repo.update(book_fixture, book_fixture.id, uow.session)
    with UnitOfWork(MembersRepo()) as uow:
        uow.repo.delete(member_fixture.id, uow.session)


def test_update_book(book_fixture):
    books_service = BooksServices()
    updated_book = Book(id=book_fixture.id, title='Updated Title', author='Updated Author')
    message, status_code = books_service.update(book_fixture.id, updated_book)
    assert status_code == 200
    assert message['message'] == 'Book updated successfully'
    updated_book_from_db, _ = books_service.get_by_id(book_fixture.id)
    assert updated_book_from_db.title == updated_book.title
    assert updated_book_from_db.author == updated_book.author


def test_delete_book(book_fixture):
    books_service = BooksServices()
    message, status_code = books_service.delete(book_fixture.id)
    assert status_code == 200
    assert message['message'] == 'Book deleted successfully'
    try:
        books_service.get_by_id(book_fixture.id)
    except ValueError:
        pass


def test_return_book(book_fixture, member_fixture):
    books_service = BooksServices()
    books_service.borrow(book_fixture.id, member_fixture.id)
    book, message, status_code = books_service.return_book(book_fixture.id)
    assert status_code == 200
    assert message['message'] == f'book with title {book.title} is now available for borrowing.'
    assert book.is_borrowed is False
    assert book.borrowed_by is None
