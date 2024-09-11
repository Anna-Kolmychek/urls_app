from fastapi import FastAPI

from .router import router
from .database import async_engine, Base

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def create_tables():
    """"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

