import random
import string

from sqlalchemy import select

from src import models
from src.constants import SHORT_URL_LEN


async def create_short_url(db) -> str:
    """Create unique short URL id"""
    short_url_len = SHORT_URL_LEN
    while True:
        shorten_url_id = ''.join(random.choices(
            string.ascii_lowercase,
            k=short_url_len
        ))
        items = select(models.UrlItem).where(
            models.UrlItem.shorten_url_id == shorten_url_id
        )
        result = await db.execute(items)
        if not result.scalars().first():
            break
        short_url_len += 1

    return shorten_url_id
