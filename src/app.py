from flask import Flask, request

from src.configs.http_status import (
    NOT_FOUND,
    BAD_REQUEST
)

from src.middlewares.common.verify_device_field import verify_device_field
from src.middlewares.common.cors import cors_middleware
from src.rate_limiters.global_rate_limiter import global_limiter

from src.routes.index import register_routes

from src.middlewares.common.malformed_json import (
    malformed_json_handler
)

from src.middlewares.common.unknown_route import (
    unknown_route_handler
)


app = Flask(__name__)


# 1. CORS
cors_middleware(app)


# 2. Global rate limiter
@app.before_request
def apply_global_rate_limiter():
    return global_limiter()


# 3. JSON parser / malformed JSON check
@app.before_request
def validate_json_request():

    if (
        request.method in ["POST", "PUT", "PATCH"]
        and request.is_json
    ):
        request.get_json()


# 4. Cookie parser
# Flask provides cookies through request.cookies


# 5. Malformed JSON handler
app.register_error_handler(
    BAD_REQUEST,
    malformed_json_handler
)


# 6. Routes
register_routes(app)


# 7. Unknown route handler
app.register_error_handler(
    NOT_FOUND,
    unknown_route_handler
)