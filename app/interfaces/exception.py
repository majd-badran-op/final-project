from flask import json, Response
from werkzeug.exceptions import HTTPException
from psycopg2 import OperationalError, IntegrityError
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError


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
        return Response(
            json.dumps(response), status=500, content_type='application/json'
        )

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e: IntegrityError):
        if 'members_email_key' in str(e.orig):
            raise ValueError('This email is already registered. Please use a different email.')
        response = {
            'code': 400,
            'name': 'IntegrityError',
            'description': f'A database integrity error occurred: {str(e)}',
        }
        return Response(
            json.dumps(response), status=400, content_type='application/json'
        )

    @app.errorhandler(SQLAlchemyIntegrityError)
    def handle_sqlalchemy_integrity_error(e: SQLAlchemyIntegrityError):
        response = {
            'code': 400,
            'name': 'IntegrityError',
            'description': f'A database integrity error occurred: {str(e)}',
        }
        return Response(
            json.dumps(response), status=400, content_type='application/json'
        )

    @app.errorhandler(ValueError)
    def handle_value_error(e: ValueError):
        response = {
            'code': 400,
            'name': 'ValueError',
            'description': f'Value error: {str(e)}',
        }
        return Response(
            json.dumps(response), status=400, content_type='application/json'
        )

    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        response = {
            'code': 500,
            'name': 'InternalServerError',
            'description': str(e),
        }
        return Response(
            json.dumps(response), status=500, content_type='application/json'
        )
