from unittest import skip

import sqlalchemy.exc
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from core import schema
from models.user_models import New_User_Container, Update_User_Container


class UserRepository:
    def __init__(self, connection: AsyncConnection):
        self.connection = connection

    async def add(self, *, container: New_User_Container):
        try:
            inserted_user = await self.connection.execute(insert(schema.users).values(**container.dict()))
            await self.connection.commit()
            return inserted_user.lastrowid
        except sqlalchemy.exc.IntegrityError as e:
            await self.connection.rollback()
            raise sqlalchemy.exc.IntegrityError(e.orig, e.params, e.statement)

    async def get_by_id(self, *, _id: int):
        return await self.connection.execute(select(
            schema.users.c.name,
            schema.users.c.email,
            schema.users.c.created_at,
            schema.users.c.updated_at
        ).where(schema.users.c.id == _id))

    async def update(self, *, _id: int, container: Update_User_Container):
        try:
            updated_user = await self.connection.execute(
                update(schema.users).values(**container.dict(exclude_none=True)).where(schema.users.c.id == _id)
            )
            await self.connection.commit()
            return updated_user.rowcount
        except sqlalchemy.exc.IntegrityError as e:
            await self.connection.rollback()
            raise sqlalchemy.exc.IntegrityError(e.orig, e.params, e.statement)

    async def get_list(self, *, skip: int, limit: int):
        return await self.connection.execute(
            select(
                schema.users.c.id,
                schema.users.c.name,
                schema.users.c.email).offset(skip).limit(limit)
        )
