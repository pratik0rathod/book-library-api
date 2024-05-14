from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from book_management.core import config


class AsyncDataBaseManager:
    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_maker = None

    def init_db(self):
        self.engine = create_async_engine(
            url=config.settings.DATABASE_URI.unicode_string()
        )

        self.session_maker = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )

    async def close(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager engine not initialized")
        await self.engine.dispose()

# async_sessionmanager = AsyncDataBaseManager()
