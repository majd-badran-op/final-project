from flask import json, Response
from psycopg2 import OperationalError, IntegrityError as Psycopg2IntegrityError
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError


def register_error_handlers(app):

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

    @app.errorhandler(Psycopg2IntegrityError)
    def handle_psycopg2_integrity_error(e: Psycopg2IntegrityError):
        if hasattr(e, 'pgcode') and e.pgcode and 'members_email_key' in e.pgcode:
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
            'name': 'CustomError',
            'description': str(e),
        }
        return Response(
            json.dumps(response), status=500, content_type='application/json'
        )
