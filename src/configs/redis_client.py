# src/configs/redis_client.py

import os
import redis

from src.utils.time_stamps import log_with_time


def get_redis_client():

    try:
        redis_host = os.getenv("REDIS_HOST")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        redis_password = os.getenv("REDIS_PASSWORD")
        redis_tls = os.getenv("REDIS_TLS", "false").lower() == "true"

        if not redis_host:
            raise ValueError("REDIS_HOST is not configured")

        protocol = "rediss" if redis_tls else "redis"

        redis_url = (
            f"{protocol}://:"
            f"{redis_password}@"
            f"{redis_host}:{redis_port}/{redis_db}"
        )

        redis_client = redis.from_url(
            redis_url,
            decode_responses=True
        )

        redis_client.ping()

        log_with_time(
            "✅ Redis connected successfully"
        )

        return redis_client

    except Exception as error:

        log_with_time(
            f"❌ Redis connection failed: {str(error)}"
        )

        raise error