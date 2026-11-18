import os
import redis
import json

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

STREAM_NAME = "url_analytics_stream"

def cache_url(short_code: str, original_url: str):
    redis_conn.setex(f"url:{short_code}", 3600, original_url)

def get_cached_url(short_code: str):
    return redis_conn.get(f"url:{short_code}")

def publish_analytics(url_id: int, ip: str, user_agent: str):
    data = {"url_id": url_id, "ip": ip, "user_agent": user_agent}
    redis_conn.xadd(STREAM_NAME, data)