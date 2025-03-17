from flask import Flask
from .view.members_view import MemberView
from .view.books_view import BookView
from flask_cors import CORS
from .view.borrow_view import BorrowView
from .view.return_view import ReturnView
from .view.member_book import MemberBookView


def register_routes(app: Flask) -> None:
    book_view = BookView.as_view('book_view')
    app.add_url_rule('/books', view_func=book_view, methods=['GET', 'POST'])
    app.add_url_rule('/books/<string:book_id>', view_func=book_view, methods=['GET', 'patch', 'DELETE'])

    borrow_view = BorrowView.as_view('borrow_view')
    app.add_url_rule('/borrow/<string:book_id>/<string:member_id>', view_func=borrow_view, methods=['POST'])

    return_view = ReturnView.as_view('return_view')
    app.add_url_rule('/return/<string:book_id>', view_func=return_view, methods=['POST'], endpoint='return_view')

    member_book = MemberBookView.as_view('return_book')
    app.add_url_rule('/member-books/<string:member_id>', view_func=member_book, methods=['GET'], endpoint='return_book')

    member_view = MemberView.as_view('member_view')
    app.add_url_rule('/members', view_func=member_view, methods=['GET', 'POST'])
    app.add_url_rule('/members/<string:member_id>', view_func=member_view, methods=['GET', 'patch', 'DELETE'])


def setup_cors(app: Flask) -> None:
    CORS(app, resources={r'/*': {'origins': '*'}}, methods=['GET', 'POST', 'PUT', 'DELETE'])
