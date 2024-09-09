from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas
from .database import async_engine, get_db, Base

app = FastAPI()


@app.on_event("startup")
async def create_tables():
    """"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post(
    "/",
    response_model=schemas.UrlItem,
    status_code=status.HTTP_201_CREATED,
    summary="Create url item",
)
async def create_url(url_item: schemas.UrlItemCreate, db: AsyncSession = Depends(get_db)):
    """Get the URL, create it's short version and save all in database."""
    db_url_item = await crud.get_url_item_by_origin(db, origin_url=url_item.origin_url)
    if db_url_item:
        raise HTTPException(status_code=400, detail="Url already registered")
    url_item = await crud.create_url_item(db=db, url_item=url_item)
    return url_item


@app.get(
    "/{url_item_id}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary="Redirect to a short URL",
)
async def read_url(url_item_id: int, db: AsyncSession = Depends(get_db)):
    """Get id for url item and redirect to a short URL with this id."""
    db_url_item = await crud.get_url_item(db, url_item_id=url_item_id)
    if db_url_item is None:
        raise HTTPException(status_code=404, detail="Url not found")
    return RedirectResponse(url=db_url_item.short_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
