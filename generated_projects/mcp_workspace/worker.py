import time
import redis
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, redis_client

def process_analytics():
    db = SessionLocal()
    r = redis_client.redis_conn
    stream_name = redis_client.STREAM_NAME
    group_name = "analytics_group"

    try:
        r.xgroup_create(stream_name, group_name, id="0", mkstream=True)
    except redis.exceptions.ResponseError:
        pass

    print("Worker started, listening for events...")
    while True:
        try:
            streams = r.xreadgroup(group_name, "worker_1", {stream_name: ">"}, count=10, block=5000)
            for stream, messages in streams:
                for message_id, data in messages:
                    analytics_entry = models.Analytics(
                        url_id=int(data["url_id"]),
                        ip_address=data["ip"],
                        user_agent=data["user_agent"]
                    )
                    db.add(analytics_entry)
                    db.commit()
                    r.xack(stream_name, group_name, message_id)
        except Exception as e:
            print(f"Error processing stream: {e}")
            time.sleep(5)

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    process_analytics()