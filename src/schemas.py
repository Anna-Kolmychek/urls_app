from pydantic import BaseModel, HttpUrl


class UrlItemBase(BaseModel):
    origin_url: HttpUrl


class UrlItemCreate(UrlItemBase):
    pass


class UrlItem(UrlItemBase):
    short_url: HttpUrl
    id: int

    class Config:
        orm_mode = True
