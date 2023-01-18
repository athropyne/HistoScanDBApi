from fastapi import FastAPI
import uvicorn

from core import config
from core.db import engine, metadata
from routes.image_router import ImageRouter
from routes.user_router import UserRouter

app = FastAPI(debug=False)
app.include_router(UserRouter("user").router)
app.include_router(ImageRouter("image").router)



async def init_db():
    async with engine.connect() as connection:
        await connection.run_sync(metadata.create_all)
    await engine.dispose()


@app.on_event("startup")
async def startup():
    await init_db()


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
    )
