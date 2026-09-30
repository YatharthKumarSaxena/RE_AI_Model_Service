# routes/llm_routes.py

from flask import Blueprint

from src.configs.uris import LLM_ROUTES

from src.middlewares.common.verify_device_field import (
    verify_device_field
)

from src.middlewares.llm.required_fields_middleware import (
    required_fields_middlewares
)

from src.middlewares.llm.field_validation_middleware import (
    validation_middlewares
)

from src.controllers.llm.convert_content_to_English import (
    convert_content_to_english_controller
)


llm_router = Blueprint(
    "llm_router",
    __name__
)


CONVERT_CONTENT_TO_ENGLISH = LLM_ROUTES[
    "CONVERT_CONTENT_TO_ENGLISH"
]


# ============================================================
# CONTENT CONVERSION
# ============================================================

@llm_router.route(
    CONVERT_CONTENT_TO_ENGLISH,
    methods=["POST"]
)
def convert_content_to_english():

    middlewares = [
        verify_device_field,
        required_fields_middlewares[
            "convert_content_to_english_required_fields_middleware"
        ],
        validation_middlewares[
            "convert_content_to_english_validation_middleware"
        ]
    ]

    for middleware in middlewares:

        result = middleware()

        if result is not None:
            return result

    return convert_content_to_english_controller()