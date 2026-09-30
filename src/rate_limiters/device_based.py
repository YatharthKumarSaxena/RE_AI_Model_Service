# rate_limiters/device_based_rate_limiters.py

from src.rate_limiters.create_redis_device_rate_limiter import (
    create_redis_device_rate_limiter
)
from src.configs.rate_limit import per_device


# Malformed / wrong request rate limiter
malformed_and_wrong_request_rate_limiter = (
    create_redis_device_rate_limiter(
        per_device["malformed_request"]
    )
)

# Unknown route rate limiter
unknown_route_limiter = (
    create_redis_device_rate_limiter(
        per_device["unknown_route"]
    )
)


device_based_rate_limiters = {
    "malformed_and_wrong_request_rate_limiter":
        malformed_and_wrong_request_rate_limiter,

    "unknown_route_limiter":
        unknown_route_limiter
}