# middlewares/common/cors_middleware.py

import os

from flask import request, make_response
from src.configs.http_status import OK


def cors_middleware(app):

    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL")
    ]

    allowed_origins = [
        origin for origin in allowed_origins
        if origin
    ]

    @app.before_request
    def handle_cors():

        origin = request.headers.get("Origin")
        request_method = request.method

        # Check if origin is allowed
        if origin in allowed_origins:
            # Store origin for after_request
            request.cors_allowed_origin = origin

        # Handle preflight requests
        if request_method == "OPTIONS":

            response = make_response("", OK)

            if origin in allowed_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"

            response.headers["Access-Control-Allow-Methods"] = (
                "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            )

            response.headers["Access-Control-Allow-Headers"] = (
                "Content-Type, Authorization, X-Requested-With, "
                "x-access-token, x-token-refreshed, x-device-uuid, "
                "x-device-type, x-device-name, x-request-id"
            )

            response.headers["Access-Control-Max-Age"] = "86400"

            return response

    @app.after_request
    def add_cors_headers(response):

        origin = request.headers.get("Origin")

        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"

        return response