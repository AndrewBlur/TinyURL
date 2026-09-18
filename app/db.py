import os

from dotenv import load_dotenv
from sqlalchemy.orm import  declarative_base 
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
load_dotenv()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_DATABASE = os.environ["POSTGRES_DB"]

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:5432/{POSTGRES_DATABASE}"
)

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False,
    bind=engine
)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

Base = declarative_base()