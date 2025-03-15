from app.tests.fake import BookFactory
import pytest
import requests


@pytest.fixture
def book_fixture():
    return BookFactory()


BASE_URL = 'http://localhost:5000/books'
id: int


def test_create_book(book_fixture):
    data = {'title': book_fixture.title, 'author': book_fixture.author}
    response = requests.post(BASE_URL, json=data)
    response_json = response.json()
    global id
    id = response_json['books']['id']
    assert response_json['code'] == 200


def test_get_books():
    response = requests.get(BASE_URL)
    response_json = response.json()
    assert response_json['code'] == 200
    assert isinstance(response_json['books'], list)


def test_get_book_by_id():
    global id
    response = requests.get(f'{BASE_URL}/{id}')
    response_json = response.json()
    assert response_json['code'] == 200
    assert isinstance(response.json(), dict)


def test_update_book(book_fixture):
    global id
    data = {'title': 'Updated Title', 'author': 'Updated Author'}
    response = requests.put(f'{BASE_URL}/{id}', json=data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['message'] == {'message': 'Book updated successfully'}


def test_delete_book(book_fixture):
    global id
    response = requests.delete(f'{BASE_URL}/{id}')
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['message'] == {'message': 'Book deleted successfully'}


def test_delete_book_that_is_not_found(book_fixture):
    global id
    response = requests.delete(f'{BASE_URL}/{id}')
    print(response.text)
    response_json = response.json()
    assert response_json == {'code': 500, 'description': 'Book not found', 'name': 'CustomError'}


def test_update_book_that_is_not_found(book_fixture):
    global id
    data = {'title': 'Updated Title', 'author': 'Updated Author'}
    response = requests.put(f'{BASE_URL}/{id}', json=data)
    print(response.text)
    response_json = response.json()
    assert response_json == {'code': 500, 'description': 'Book not found', 'name': 'CustomError'}
