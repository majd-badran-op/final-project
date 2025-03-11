from flask import Flask
from view.members_view import MemberView
from view.bocks_view import BookView
from flask_cors import CORS


def register_routes(app: Flask):
    book_view = BookView.as_view('book_view')
    app.add_url_rule('/books', view_func=book_view, methods=['GET', 'POST'])
    app.add_url_rule('/books/<int:book_id>', view_func=book_view, methods=['GET', 'PUT', 'DELETE'])
    app.add_url_rule('/borrow/<int:book_id>/<uuid:member_id>', view_func=book_view, methods=['POST'])
    app.add_url_rule('/return/<int:book_id>', view_func=book_view, methods=['POST'])

    member_view = MemberView.as_view('member_view')
    app.add_url_rule('/members', view_func=member_view, methods=['GET', 'POST'])
    app.add_url_rule('/members/<uuid:member_id>', view_func=member_view, methods=['GET', 'PUT', 'DELETE'])


def setup_cors(app):
    CORS(app, resources={r'/*': {'origins': '*'}}, methods=['GET', 'POST', 'PUT', 'DELETE'])
