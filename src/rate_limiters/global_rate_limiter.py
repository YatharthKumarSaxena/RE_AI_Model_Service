# rate_limiters/global_rate_limiter.py

import os
import time

from flask import request, jsonify

from src.utils.time_stamps import log_with_time
from src.utils.log_error import error_message
from src.configs.http_status import TOO_MANY_REQUESTS, INTERNAL_ERROR
from src.configs.redis_client import get_redis_client


def create_global_limiter():

    try:
        redis_client = get_redis_client()

        window_minutes = int(
            os.getenv("RATE_LIMIT_WINDOW", 10)
        )

        max_requests = int(
            os.getenv("RATE_LIMIT_MAX", 100)
        )

        window_seconds = window_minutes * 60

        def global_limiter():

            try:
                ip = (
                    request.remote_addr
                    or request.headers.get("X-Forwarded-For")
                    or "UNKNOWN_IP"
                )

                path = request.path

                key = f"global-rate-limit:{ip}"

                current_count = redis_client.incr(key)

                if current_count == 1:
                    redis_client.expire(
                        key,
                        window_seconds
                    )

                if current_count > max_requests:

                    ttl = redis_client.ttl(key)

                    retry_after_seconds = (
                        ttl if ttl > 0 else None
                    )

                    log_with_time(
                        f"🚫 Global Rate Limit Triggered | "
                        f"IP: {ip} | Path: {path}"
                    )

                    response = jsonify({
                        "success": False,
                        "message": (
                            "Too many requests. "
                            "Please try again after some time."
                        )
                    })

                    response.status_code = TOO_MANY_REQUESTS

                    if retry_after_seconds is not None:
                        response.headers["Retry-After"] = str(
                            retry_after_seconds
                        )

                    return response

                return None

            except Exception as err:
                error_message(err)

                return jsonify({
                    "success": False,
                    "message": "Internal Server Error in Global Limiter"
                }), INTERNAL_ERROR

        return global_limiter

    except Exception as err:

        error_message(err)

        def fallback_global_limiter():

            return jsonify({
                "success": False,
                "message": "Internal Server Error"
            }), INTERNAL_ERROR

        return fallback_global_limiter


global_limiter = create_global_limiter()