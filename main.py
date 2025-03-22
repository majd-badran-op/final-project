from fastapi import FastAPI
from app.presentation.routes.book_routes import book_router
from app.presentation.routes.member_routes import member_router
from app.presentation.exception_handler import register_error_handlers

app = FastAPI()

app.include_router(book_router, prefix='/v1/books', tags=['Books'])

app.include_router(member_router, prefix='/v1/members', tags=['Members'])

register_error_handlers(app)
