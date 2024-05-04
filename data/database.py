from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine("sqlite+aiosqlite:///data/ruspanol.db")

session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase):
    type_annotation_map = {
        # Custom types here
    }
