from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .utils import create_short_url


async def get_url_item_by_origin(db: AsyncSession,
                                 origin_url: str,
                                 ) -> models.UrlItem:
    """Get record from DB by origin URL."""

    items = select(models.UrlItem).where(
        models.UrlItem.origin_url == str(origin_url))
    result = await db.execute(items)
    return result.scalars().first()


async def get_url_item_by_shorten(db: AsyncSession,
                                  shorten_url_id: str,
                                  ) -> models.UrlItem:
    """Get record from DB by shorten URL id."""

    items = select(models.UrlItem).where(
        models.UrlItem.shorten_url_id == shorten_url_id)
    result = await db.execute(items)
    return result.scalars().first()


async def create_url_item(db: AsyncSession,
                          url_item: schemas.UrlItemCreate,
                          ) -> models.UrlItem:
    """Get origin URL, create unique shorten URL, create record in DB."""

    origin_url = url_item.origin_url
    shorten_url_id = await create_short_url(db)

    db_url_item = models.UrlItem(
        origin_url=str(origin_url),
        shorten_url_id=shorten_url_id,
    )

    db.add(db_url_item)
    await db.commit()
    await db.refresh(db_url_item)
    return db_url_item
