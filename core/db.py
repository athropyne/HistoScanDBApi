from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from core import config

engine: AsyncEngine = create_async_engine(config.SQLITE_URL, echo=config.DB_DEBUG)
metadata = MetaData()


async def get_connection():
    connection = await engine.connect()
    try:
        yield connection
    finally:
        await connection.close()
