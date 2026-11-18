
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from prometheus_fastapi_instrumentator import Instrumentator

from .database import get_db, engine, Base
from .schemas import URLCreate, URLResponse, AnalyticsResponse
from .crud import create_url, get_url_by_code, get_analytics
from .redis_client import redis_conn
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Initialize database tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Verify Redis connectivity
        await redis_conn.ping()

        print("AEGIS URL Shortener started successfully.")

        yield

    finally:
        # Close Redis connection
        await redis_conn.aclose()

        # Dispose database engine
        await engine.dispose()

        print("AEGIS URL Shortener shut down.")


app = FastAPI(
    title="URL Shortener",
    description="AEGIS-generated URL Shortening Application",
    version="1.0.0",
    lifespan=lifespan
)

Instrumentator().instrument(app).expose(app)


@app.post("/api/v1/urls", response_model=URLResponse)
async def shorten_url(
    payload: URLCreate,
    db: AsyncSession = Depends(get_db)
):
    url_obj = await create_url(db, str(payload.url))

    cache_data = {
        "url_id": url_obj.id,
        "original_url": url_obj.original_url
    }

    await redis_conn.set(
        f"url:{url_obj.short_code}",
        json.dumps(cache_data),
        ex=3600
    )

    return url_obj


@app.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    cache_key = f"url:{short_code}"

    cached_data = await redis_conn.get(cache_key)

    if cached_data:
        cache_data = json.loads(cached_data)

        url_id = int(cache_data["url_id"])
        original_url = cache_data["original_url"]

    else:
        url_obj = await get_url_by_code(db, short_code)

        if not url_obj:
            raise HTTPException(
                status_code=404,
                detail="URL not found"
            )

        url_id = url_obj.id
        original_url = url_obj.original_url

        cache_data = {
            "url_id": url_id,
            "original_url": original_url
        }

        await redis_conn.set(
            cache_key,
            json.dumps(cache_data),
            ex=3600
        )

    analytics_data = {
        "url_id": str(url_id),
        "ip_address": (
            request.client.host if request.client else "unknown"
        ),
        "user_agent": request.headers.get(
            "user-agent",
            "unknown"
        )
    }

    await redis_conn.xadd(
        settings.STREAM_NAME,
        analytics_data
    )

    return RedirectResponse(url=original_url)


@app.get(
    "/api/v1/urls/{url_id}/analytics",
    response_model=list[AnalyticsResponse]
)
async def fetch_analytics(
    url_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_analytics(db, url_id)
