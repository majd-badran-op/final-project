from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from psycopg2 import OperationalError, IntegrityError as Psycopg2IntegrityError
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(OperationalError)
    async def handle_database_exception(request, exc: OperationalError):
        response = {
            'code': 500,
            'name': 'DatabaseError',
            'description': str(exc),
        }
        return JSONResponse(content=response, status_code=500)

    @app.exception_handler(Psycopg2IntegrityError)
    async def handle_psycopg2_integrity_error(request, exc: Psycopg2IntegrityError):
        if hasattr(exc, 'pgcode') and exc.pgcode and 'members_email_key' in exc.pgcode:
            raise HTTPException(status_code=400,
                                detail='This email is already registered. Please use a different email.')
        response = {
            'code': 400,
            'name': 'IntegrityError',
            'description': f'A database integrity error occurred: {str(exc)}',
        }
        return JSONResponse(content=response, status_code=400)

    @app.exception_handler(SQLAlchemyIntegrityError)
    async def handle_sqlalchemy_integrity_error(request, exc: SQLAlchemyIntegrityError):
        response = {
            'code': 400,
            'name': 'IntegrityError',
            'description': f'A database integrity error occurred: {str(exc)}',
        }
        return JSONResponse(content=response, status_code=400)

    @app.exception_handler(ValueError)
    async def handle_value_error(request, exc: ValueError):
        response = {
            'code': 400,
            'name': 'ValueError',
            'description': f'Value error: {str(exc)}',
        }
        return JSONResponse(content=response, status_code=400)

    @app.exception_handler(Exception)
    async def handle_generic_exception(request, exc: Exception):
        response = {
            'code': 500,
            'name': type(exc).__name__,
            'description': str(exc),
        }
        return JSONResponse(content=response, status_code=500)
