import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()
# SERVER
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
UPLOADED_IMAGES_PATH = "images/"


# DATABASE
class DB_Types(str, Enum):
    MYSQL = "mysql"
    POSTGRESQL = ""


DB_TYPE = DB_Types.MYSQL
DB_DRIVER = "asyncmy"
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_CONNECT_URL = f"{DB_Types.MYSQL}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_DEBUG = True

SQLITE_URL = 'sqlite+aiosqlite:///./db.db'
