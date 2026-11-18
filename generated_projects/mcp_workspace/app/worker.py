
import asyncio
import logging
import os
import socket

from redis.exceptions import ResponseError
from sqlalchemy.dialects.postgresql import insert

from .database import SessionLocal, engine
from .models import Analytics
from .redis_client import redis_conn
from .config import settings


# Worker configuration
BATCH_SIZE = 10
BLOCK_TIME_MS = 2000
PENDING_IDLE_TIME_MS = 60000

CONSUMER_NAME = (
    f"worker-{socket.gethostname()}-{os.getpid()}"
)


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


async def initialize_consumer_group():
    """Create the Redis consumer group if it does not exist."""

    try:
        await redis_conn.xgroup_create(
            settings.STREAM_NAME,
            settings.GROUP_NAME,
            id="0",
            mkstream=True
        )

        logger.info("Redis consumer group created.")

    except ResponseError as exc:

        if "BUSYGROUP" in str(exc):
            logger.info(
                "Redis consumer group already exists."
            )
        else:
            raise


async def process_messages(messages):
    """Save Redis Stream messages into PostgreSQL."""

    if not messages:
        return

    records = []
    message_ids = []

    for message_id, data in messages:

        records.append({
            "url_id": int(data["url_id"]),
            "stream_message_id": message_id,
            "ip_address": data.get("ip_address"),
            "user_agent": data.get("user_agent")
        })

        message_ids.append(message_id)

    # Insert analytics records.
    # Ignore duplicate stream message IDs.
    statement = (
        insert(Analytics)
        .values(records)
        .on_conflict_do_nothing(
            index_elements=["stream_message_id"]
        )
    )

    async with SessionLocal() as db:

        try:
            await db.execute(statement)
            await db.commit()

        except Exception:
            await db.rollback()
            raise

    # Acknowledge messages only after database commit.
    acknowledged = await redis_conn.xack(
        settings.STREAM_NAME,
        settings.GROUP_NAME,
        *message_ids
    )

    logger.info(
        "Received %s events; acknowledged %s.",
        len(message_ids),
        acknowledged
    )


async def process_analytics():
    """Continuously consume and process analytics events."""

    await initialize_consumer_group()

    logger.info(
        "Analytics worker started. Consumer: %s",
        CONSUMER_NAME
    )

    claim_cursor = "0-0"

    try:

        while True:

            try:
                # Recover messages left pending by another worker.
                claim_cursor, pending_messages, _ = (
                    await redis_conn.xautoclaim(
                        settings.STREAM_NAME,
                        settings.GROUP_NAME,
                        CONSUMER_NAME,
                        min_idle_time=PENDING_IDLE_TIME_MS,
                        start_id=claim_cursor,
                        count=BATCH_SIZE
                    )
                )

                if pending_messages:
                    await process_messages(pending_messages)
                    continue

                # Read new messages from Redis Stream.
                streams = await redis_conn.xreadgroup(
                    settings.GROUP_NAME,
                    CONSUMER_NAME,
                    {settings.STREAM_NAME: ">"},
                    count=BATCH_SIZE,
                    block=BLOCK_TIME_MS
                )

                for stream, messages in streams:
                    await process_messages(messages)

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception(
                    "Analytics worker processing failed."
                )

                await asyncio.sleep(5)

    finally:
        logger.info("Analytics worker stopping.")


async def main():
    """Start the worker and clean up resources."""

    try:
        await process_analytics()

    finally:

        try:
            await redis_conn.aclose()

        finally:
            await engine.dispose()

        logger.info("Worker resources closed.")


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("Worker interrupted.")
