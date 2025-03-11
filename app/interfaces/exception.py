from flask import json
from werkzeug.exceptions import HTTPException
from psycopg2 import OperationalError


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        response = e.get_response()
        response.data = json.dumps({
            'code': e.code,
            'name': e.name,
            'description': e.description,
        })
        response.content_type = 'application/json'
        return response

    @app.errorhandler(OperationalError)
    def handle_database_exception(e: OperationalError):
        response = {
            'code': 500,
            'name': 'DatabaseError',
            'description': str(e),
        }
        return json.dumps(response), 500

    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        response = {
            'code': 500,
            'name': 'InternalServerError',
            'description': str(e),
        }
        return json.dumps(response), 500
