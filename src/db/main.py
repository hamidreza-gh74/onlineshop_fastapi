
from typing import AsyncGenerator
from sqlmodel import create_engine,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


async_engine = AsyncEngine(
    create_engine(
    url=config.DATABASE_URL
)
)


# async def init_db():
#     async with async_engine.begin() as conn:
#         from src.books.models import Book

#         await conn.run_sync(SQLModel.metadata.create_all)

        

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=async_engine,
        class_= AsyncSession,
        expire_on_commit= False
    )
    
    async with Session() as session:
        yield session