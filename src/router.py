from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.UrlItem,
    status_code=status.HTTP_201_CREATED,
    summary="Create url item",
)
async def create_url(
        url_item: schemas.UrlItemCreate,
        db: AsyncSession = Depends(get_db)
):
    """Get the URL, create it's short version and save all in database."""
    db_url_item = await crud.get_url_item_by_origin(
        db,
        origin_url=url_item.origin_url
    )
    if db_url_item:
        raise HTTPException(status_code=400, detail="Url already registered")
    url_item = await crud.create_url_item(db, url_item=url_item)
    return url_item


@router.get(
    "/{shorten_url_id}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary="Redirect to a short URL",
)
async def read_url(shorten_url_id: str, db: AsyncSession = Depends(get_db)):
    """Get id for url item and redirect to a short URL with this id."""
    db_url_item = await crud.get_url_item_by_shorten(
        db,
        shorten_url_id=shorten_url_id
    )
    if db_url_item is None:
        raise HTTPException(status_code=404, detail="Url not found")
    return RedirectResponse(
        url=db_url_item.origin_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
