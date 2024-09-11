from sqlalchemy import Column, Integer, String

from .constants import MAX_STR_LEN
from .database import Base


class UrlItem(Base):
    __tablename__ = "url_items"

    id = Column(Integer, primary_key=True)
    origin_url = Column(String(MAX_STR_LEN), unique=True)
    shorten_url_id = Column(String(MAX_STR_LEN), unique=True)
