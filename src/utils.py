import requests
from fastapi import HTTPException
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_url_item(db: AsyncSession, url_item_id: int) -> models.UrlItem:
    items = select(models.UrlItem).where(models.UrlItem.id == url_item_id)
    result = await db.execute(items)
    return result.scalars().first()


async def get_url_item_by_origin(db: AsyncSession, origin_url: str) -> models.UrlItem:
    items = select(models.UrlItem).where(models.UrlItem.origin_url == str(origin_url))
    result = await db.execute(items)
    return result.scalars().first()


async def create_url_item(db: AsyncSession, url_item: schemas.UrlItemCreate) -> models.UrlItem:
    origin_url = url_item.origin_url
    short_url = get_short_url(origin_url)

    db_url_item = models.UrlItem(
        origin_url=str(origin_url),
        short_url=str(short_url),
    )

    db.add(db_url_item)
    await db.commit()
    await db.refresh(db_url_item)
    return db_url_item


def get_short_url(origin_url) -> HttpUrl:
    short_url_maker = 'https://clck.ru/--'
    response = requests.get(
        short_url_maker,
        params={'url': origin_url}
    )
    if response.status_code == 400 and response.text == 'Invalid URL':
        raise HTTPException(status_code=400, detail="Invalid URL")
    elif response.status_code == 200:
        return response.text
    else:
        raise HTTPException(status_code=400, detail="Can't get short url")
