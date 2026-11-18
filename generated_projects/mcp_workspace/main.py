from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator
import models, schemas, crud, database, redis_client

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="URL Shortener API")

Instrumentator().instrument(app).expose(app)

@app.post("/api/v1/urls", response_model=schemas.URLResponse)
def shorten_url(url_in: schemas.URLCreate, db: Session = Depends(database.get_db)):
    db_url = crud.create_url(db, url_in)
    redis_client.cache_url(db_url.short_code, db_url.original_url)
    return db_url

@app.get("/{short_code}")
def redirect_to_url(short_code: str, request: Request, db: Session = Depends(database.get_db)):
    original_url = redis_client.get_cached_url(short_code)
    
    if not original_url:
        db_url = crud.get_url_by_short_code(db, short_code)
        if not db_url:
            raise HTTPException(status_code=404, detail="URL not found")
        original_url = db_url.original_url
        redis_client.cache_url(short_code, original_url)
        url_id = db_url.id
    else:
        db_url = crud.get_url_by_short_code(db, short_code)
        url_id = db_url.id if db_url else None

    if url_id:
        redis_client.publish_analytics(
            url_id=url_id,
            ip=request.client.host,
            user_agent=request.headers.get("user-agent", "unknown")
        )

    return RedirectResponse(url=original_url)

@app.get("/api/v1/urls/{url_id}/analytics", response_model=schemas.AnalyticsResponse)
def get_url_analytics(url_id: int, db: Session = Depends(database.get_db)):
    return crud.get_analytics(db, url_id)