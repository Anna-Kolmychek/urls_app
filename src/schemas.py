from pydantic import BaseModel, HttpUrl


class UrlItemBase(BaseModel):
    origin_url: HttpUrl


class UrlItemCreate(UrlItemBase):
    pass


class UrlItem(UrlItemBase):
    shorten_url_id: str
    id: int

    class Config:
        orm_mode = True
