# Library Management System

## Overview
This is a Flask-based library management system that allows users to manage books, members, and borrowing transactions. The application provides a RESTful API to perform CRUD operations on books and members, as well as functionalities for borrowing and returning books.

## Setup and Installation

### 1. Create a Virtual Environment with Pyenv
Ensure you have `pyenv` installed, then create a virtual environment:
```sh
pyenv virtualenv 3.10.4 library_env
pyenv activate library_env
```

### 2. Install Dependencies
Install the required packages using `requirements.txt`:
```sh
pip install -r requirements.txt
```

### 3. Run the Flask Application
Start the local Flask server:
```sh
python -m main
```

## API Endpoints

### Books
#### List all books
```sh
curl -X GET http://localhost:5000/books
```

#### Add a new book
```sh
curl -X POST http://localhost:5000/books \
    -H "Content-Type: application/json" \
    -d '{"title": "Millionaire", "author": "Majd Badaran"}'
```

#### Get a book by ID
```sh
curl -X GET http://localhost:5000/books/213
```

#### Update a book
```sh
curl -X PUT http://localhost:5000/books/258 \
    -H "Content-Type: application/json" \
    -d '{"title": "Updated Book", "author": "Updated Author"}'
```

#### Delete a book
```sh
curl -X DELETE http://localhost:5000/books/9
```

### Borrowing & Returning Books
#### Borrow a book
```sh
curl -X POST http://localhost:5000/borrow/4/8822b74b-185f-4f7d-93d5-267873749473
```

#### Return a borrowed book
```sh
curl -X POST http://localhost:5000/return/4
```

### Members
#### List all members
```sh
curl -X GET http://localhost:5000/members
```

#### Add a member
```sh
curl -X POST http://localhost:5000/members \
    -H "Content-Type: application/json" \
    -d '{"name": "Badran", "email": "test@gmail.com"}'
```

#### Get a member by ID
```sh
curl -X GET http://localhost:5000/members/85
```

#### Update a member
```sh
curl -X PATCH http://localhost:5000/members/8822b74b-185f-4f7d-93d5-267873749473 \
    -H "Content-Type: application/json" \
    -d '{"name": "majd badran"}'
```

#### Delete a member
```sh
curl -X DELETE http://localhost:5000/members/8822b74b-185f-4f7d-93d5-267873749473
```

#### List all books borrowed by a member
```sh
curl -X GET http://localhost:5000/member-books/8822b74b-185f-4f7d-93d5-267873749473
```

## Running Tests
To run the test suite with `pytest`, execute the following command:
```sh
PYTHONPATH=$(pwd) pytest app/tests
```

