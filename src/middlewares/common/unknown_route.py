# middlewares/handlers/unknown_route_handler.py

from flask import jsonify, request

from src.configs.http_status import NOT_FOUND
from src.utils.time_stamps import log_with_time
from src.rate_limiters.device_based import (
    device_based_rate_limiters
)

unknown_route_limiter = (
    device_based_rate_limiters[
        "unknown_route_limiter"
    ]
)

def unknown_route_handler(error):

    log_with_time(
        f"❌ Unknown route hit: "
        f"{request.method} {request.path}"
    )

    return unknown_route_limiter(
        request,
        lambda: (
            jsonify({
                "code": "UNKNOWN_ROUTE",
                "message": "The requested endpoint does not exist"
            }),
            NOT_FOUND
        )
    )