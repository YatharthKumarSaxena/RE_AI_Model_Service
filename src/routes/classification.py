from flask import Blueprint

from src.configs.uris import (
    CLASSIFICATION_BASE,
    CLASSIFICATION_ROUTES
)

from src.middlewares.common.verify_device_field import (
    verify_device_field
)

from src.middlewares.common.default_model_middleware import (
    set_entity_model_middleware
)

from src.middlewares.classification.field_validation_middleware import (
    validation_middlewares
)

from src.middlewares.classification.required_fields_middleware import (
    required_fields_middlewares
)

from src.middlewares.llm.content_conversion_middleware import (
    convert_content_to_english_middleware
)

from src.controllers.classification.classify_entity import (
    classify_entity_controller
)

from src.controllers.classification.entity_bulk_import import (
    import_entity_type_controller
)

from src.middlewares.bulk_import.file_upload_middleware import (
    file_upload_middlewares
)

from src.middlewares.bulk_import.parse_import_file_middleware import (
    parse_file_middlewares
)

from src.middlewares.bulk_import.validate_header_column_middleware import (
    validate_header_column_middlewares
)


classification_bp = Blueprint(
    "classification",
    __name__,
    url_prefix=CLASSIFICATION_BASE
)


# ============================================================
# ENTITY CLASSIFICATION
# ============================================================

@classification_bp.route(
    CLASSIFICATION_ROUTES["CLASSIFY_ENTITY"],
    methods=["POST"]
)
def classify_entity():

    middlewares = [
        verify_device_field,
        required_fields_middlewares[
            "classify_entity_type_required_fields_middleware"
        ],
        validation_middlewares[
            "classify_entity_type_validation_middleware"
        ],
        convert_content_to_english_middleware,
        set_entity_model_middleware
    ]

    for middleware in middlewares:

        result = middleware()

        if result is not None:
            return result

    return classify_entity_controller()


# ============================================================
# BULK ENTITY CLASSIFICATION
# ============================================================

@classification_bp.route(
    CLASSIFICATION_ROUTES["BULK_ENTITY_CLASSIFY"],
    methods=["POST"]
)
def bulk_entity_classify():

    middlewares = [
        verify_device_field,
        file_upload_middlewares[
            "check_entity_type_import_file_upload_configuration"
        ],
        parse_file_middlewares[
            "parse_entity_type_spreadsheet_file_middleware"
        ],
        validate_header_column_middlewares[
            "create_entity_type_in_bulk_header_validation_middleware"
        ],
        set_entity_model_middleware
    ]

    for middleware in middlewares:

        result = middleware()

        if result is not None:
            return result

    return import_entity_type_controller()