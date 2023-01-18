from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey

from core.db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100)),
    Column("email", String(100), unique=True),
    Column("password", String(100)),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=True)
)
svs = Table(
    "svs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("filename", String(50), nullable=False),
    Column("description", String(1000), nullable=True),
    Column("image_url", String, nullable=True),
    Column("creator_id", ForeignKey(users.c.id), nullable=False),
    Column("created_at", DateTime, nullable=False)
)



