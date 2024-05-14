from collections.abc import AsyncIterable
from datetime import datetime

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import mapped_column, Mapped

from database.database_manager import AsyncDataBaseManager


# engine = create_engine(url=config.settings.DATABASE_URI.unicode_string())
#
# session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@as_declarative()
class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, sort_order=-1)
    created_on: Mapped[datetime] = mapped_column(default=datetime.now)
    last_updated: Mapped[datetime] = mapped_column(
        onupdate=datetime.now, default=datetime.now)


# creating async db connection for database
async_sessionmanager = AsyncDataBaseManager()
async_sessionmanager.init_db()


async def create_db_table():
    await Base.metadata.create_all(async_sessionmanager.engine)


async def get_async_db() -> AsyncIterable[AsyncSession]:
    async with async_sessionmanager.session_maker() as session:
        try:
            yield session

        except Exception as e:
            print(e)
            await session.rollback()
            raise

        finally:
            await session.close()
