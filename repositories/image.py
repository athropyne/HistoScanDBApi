from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from core import schema
from models.image_models import New_Image_Container


class ImageRepository:
    def __init__(self, connection: AsyncConnection):
        self.connection = connection

    async def add(self, *, container: New_Image_Container):
        inserted_image = await self.connection.execute(insert(schema.svs).values(**container.dict()))
        await self.connection.commit()
        return inserted_image.lastrowid

    async def get_by_id(self, *, _id: int):
        return await self.connection.execute(select(schema.svs).where(schema.svs.c.id == _id))

    async def get_list(self, *, skip, limit):
        return await self.connection.execute(
            select(schema.svs,
                   schema.users.c.name.label("creator_name"))
            .join(schema.users).offset(skip).limit(limit)

        )
