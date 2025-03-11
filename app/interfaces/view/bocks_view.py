from typing import Optional
from flask import abort, jsonify, request, Response
from flask.views import MethodView
from domain.entities.book_entity import Book


class BookView(MethodView):
    ...
