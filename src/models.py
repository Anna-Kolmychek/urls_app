from sqlalchemy import Column, Integer, String

from .database import Base


class UrlItem(Base):
    __tablename__ = "url_items"

    id = Column(Integer, primary_key=True)
    origin_url = Column(String)
    short_url = Column(String)
