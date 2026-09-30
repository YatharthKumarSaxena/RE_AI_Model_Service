# rate_limiters/create_redis_device_rate_limiter.py

from flask import jsonify

from src.configs.headers import DEVICE_HEADERS
from src.configs.http_status import TOO_MANY_REQUESTS, INTERNAL_ERROR
from src.configs.redis_client import get_redis_client
from src.utils.log_error import error_message


def create_redis_device_rate_limiter(config):

    max_requests = config["max_requests"]
    window_ms = config["window_ms"]
    prefix = config["prefix"]
    reason = config.get("reason")
    message = config.get(
        "message",
        "Too many requests. Please try again later."
    )

    redis_client = get_redis_client()

    window_seconds = window_ms // 1000

    def rate_limiter(request, next_callback):

        try:
            device_id = (
                request.headers.get(
                    DEVICE_HEADERS["DEVICE_UUID"]
                )
                or getattr(request, "device_id", None)
                or "UNKNOWN_DEVICE"
            )

            key = f"{prefix}:{device_id}"

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

                response = jsonify({
                    "success": False,
                    "message": message
                })

                response.status_code = TOO_MANY_REQUESTS

                if retry_after_seconds is not None:
                    response.headers["Retry-After"] = str(
                        retry_after_seconds
                    )

                return response

            return next_callback()

        except Exception as error:

            error_message(error)

            return jsonify({
                "success": False,
                "message": "Internal Server Error in Rate Limiter"
            }), INTERNAL_ERROR

    return rate_limiter