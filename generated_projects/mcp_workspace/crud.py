from sqlalchemy.orm import Session
import models, schemas, utils

def create_url(db: Session, url_schema: schemas.URLCreate):
    short_code = utils.generate_short_code()
    db_url = models.URL(original_url=str(url_schema.url), short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url_by_short_code(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()

def get_analytics(db: Session, url_id: int):
    count = db.query(models.Analytics).filter(models.Analytics.url_id == url_id).count()
    last_click = db.query(models.Analytics.timestamp).filter(models.Analytics.url_id == url_id).order_by(models.Analytics.timestamp.desc()).first()
    return {"total_clicks": count, "last_click": last_click[0] if last_click else None}