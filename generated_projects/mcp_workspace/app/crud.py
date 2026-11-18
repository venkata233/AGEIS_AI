from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from .models import URL, Analytics
from .utils import generate_short_code


MAX_CODE_ATTEMPTS = 5


async def create_url(db: AsyncSession, original_url: str) -> URL:
    for attempt in range(MAX_CODE_ATTEMPTS):
        short_code = generate_short_code()

        db_url = URL(
            original_url=original_url,
            short_code=short_code
        )

        db.add(db_url)

        try:
            await db.commit()
            await db.refresh(db_url)
            return db_url

        except IntegrityError:
            await db.rollback()

            if attempt == MAX_CODE_ATTEMPTS - 1:
                raise RuntimeError(
                    "Unable to generate a unique short code "
                    "after multiple attempts."
                )

    raise RuntimeError("URL creation failed.")


async def get_url_by_code(
    db: AsyncSession,
    short_code: str
) -> URL | None:

    result = await db.execute(
        select(URL).where(URL.short_code == short_code)
    )

    return result.scalars().first()


async def get_analytics(db: AsyncSession, url_id: int):
    result = await db.execute(
        select(Analytics).where(Analytics.url_id == url_id)
    )

    return result.scalars().all()