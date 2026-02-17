import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/qa_microservice"
)

engine = create_async_engine(
    DATABASE_URL,
    echo = True # Print SQL queries for debugging
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

# Dependency for FastAPI endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
