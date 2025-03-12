import pytest
from app.infrastructure.repositories.unit_of_work import UnitOfWork
from app.tests.fake import MemberFactory
from app.infrastructure.repositories.members_repo import MembersRepo
from app.application.services.members_services import MembersServices
from app.domain.entities.member_entity import Member


@pytest.fixture
def member_fixture():
    member = MemberFactory()
    with UnitOfWork(MembersRepo()) as uow:
        created_member = uow.repo.insert(member, uow.session)
    yield created_member
    with UnitOfWork(MembersRepo()) as uow:
        uow.repo.delete(created_member.id, uow.session)


def test_create_member(member_fixture):
    assert member_fixture.name is not None
    assert member_fixture.email is not None


def test_get_member_by_id(member_fixture):
    member_service = MembersServices()
    member, message, status_code = member_service.get_by_id(member_fixture.id)
    assert status_code == 200
    assert member.id == member_fixture.id
    assert member.name == member_fixture.name
    assert member.email == member_fixture.email


def test_update_member(member_fixture):
    member_service = MembersServices()
    updated_member = Member(id=member_fixture.id, name='Updated name', email='Updated email')
    message, status_code = member_service.update(member_fixture.id, updated_member)
    assert status_code == 200
    assert message['message'] == 'Member updated successfully'
    updated_member_from_db, message, status_code = member_service.get_by_id(member_fixture.id)
    assert status_code == 200
    assert updated_member_from_db.name == updated_member.name
    assert updated_member_from_db.email == updated_member.email


def test_delete_member(member_fixture):
    member_service = MembersServices()
    message, status_code = member_service.delete(member_fixture.id)
    assert status_code == 200
    assert message['message'] == 'Member deleted successfully'
    try:
        member_service.get_by_id(member_fixture.id)
    except ValueError:
        pass
