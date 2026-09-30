# middlewares/handlers/malformed_json_handler.py

from flask import jsonify, request

from src.configs.http_status import BAD_REQUEST
from src.utils.time_stamps import log_with_time
from src.rate_limiters.device_based import (
    device_based_rate_limiters
)

malformed_and_wrong_request_rate_limiter = (
    device_based_rate_limiters[
        "malformed_and_wrong_request_rate_limiter"
    ]
)


def malformed_json_handler(error):

    # Check if error is related to malformed JSON
    if (
        request.method in ["POST", "PUT", "PATCH"]
        and request.is_json
        and error.code == BAD_REQUEST
    ):
        log_with_time(
            f"❌ Malformed JSON in "
            f"{request.method} {request.path}"
        )

        return malformed_and_wrong_request_rate_limiter(
            request,
            lambda: (
                jsonify({
                    "code": "MALFORMED_JSON",
                    "message": "Invalid JSON syntax in request body"
                }),
                BAD_REQUEST
            )
        )

    raise error