import pytest
import requests
from app.tests.fake import MemberFactory, BookFactory


@pytest.fixture
def member_fixture():
    return MemberFactory()


@pytest.fixture
def book_fixture():
    return BookFactory()


BASE_URL = 'http://localhost:5000/members'
id: str


def test_create_member(member_fixture):
    data = {'name': member_fixture.name, 'email': member_fixture.email}
    response = requests.post(BASE_URL, json=data)
    response_json = response.json()
    global id
    id = response_json['member']['id']
    assert response_json['code'] == 200


def test_get_members():
    response = requests.get(BASE_URL)
    response_json = response.json()
    assert response_json['code'] == 200
    assert isinstance(response.json(), dict)


def test_get_member_by_id():
    global id
    response = requests.get(f'{BASE_URL}/{id}')
    response_json = response.json()
    assert response_json['code'] == 200
    assert isinstance(response.json(), dict)


def test_update_member(member_fixture):
    global id
    data = {'name': 'Updated Name', 'email': 'updated@example.com'}
    response = requests.put(f'{BASE_URL}/{id}', json=data)
    response_json = response.json()
    assert response_json['code'] == 200
    assert response_json['message'] == {'message': 'Member updated successfully'}


def test_delete_member(member_fixture):
    global id
    response = requests.delete(f'{BASE_URL}/{id}')
    response_json = response.json()
    assert response_json['code'] == 200
    assert response_json['message'] == {'message': 'Member deleted successfully'}
