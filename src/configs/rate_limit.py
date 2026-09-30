# configs/rate_limit.py

per_device = {
    "malformed_request": {
        "max_requests": 20,
        "window_ms": 60 * 1000,  # 1 minute
        "prefix": "malformed_request",
        "reason": "Malformed request",
        "message": (
            "Too many malformed requests. "
            "Fix your payload and try again later."
        )
    },

    "unknown_route": {
        "max_requests": 10,
        "window_ms": 60 * 1000,  # 1 minute
        "prefix": "unknown_route",
        "reason": "Unknown route access",
        "message": "Too many invalid or unauthorized requests."
    }
}