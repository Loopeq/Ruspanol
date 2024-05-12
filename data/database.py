from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(settings.db_url)


session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase):
    type_annotation_map = {
        # Custom types here
    }
