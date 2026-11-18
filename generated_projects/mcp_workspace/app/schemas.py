
from datetime import datetime

from pydantic import BaseModel, HttpUrl, ConfigDict


class URLCreate(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_url: str
    short_code: str
    created_at: datetime


class AnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    ip_address: str | None = None
    user_agent: str | None = None
