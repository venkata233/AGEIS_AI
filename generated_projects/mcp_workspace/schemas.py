from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    url: HttpUrl

class URLCreate(URLBase):
    pass

class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime

    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    total_clicks: int
    last_click: Optional[datetime]

    class Config:
        from_attributes = True