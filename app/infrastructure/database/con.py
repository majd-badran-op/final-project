import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine


load_dotenv()

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
DATABASE_NAME = os.getenv('DATABASE_NAME')

DATABASE_URL = (
    f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@'
    f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
)

engine = create_async_engine(DATABASE_URL, echo=True)
