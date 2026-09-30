"""
Pure ID Validation Functions (Industry Standard)

These functions return boolean only.
NO response handling.

Middleware handles logging and HTTP responses.
"""

from src.utils.validators_factory import (
    is_valid_regex,
    validate_length
)

from src.configs.regex import (
    UUID_V4_REGEX,
    MONGO_ID_REGEX
)

from src.configs.field_lengths import (
    FIELD_LENGTHS
)


# UUID v4 validation
def is_valid_uuid(value):
    return is_valid_regex(
        value,
        UUID_V4_REGEX
    )


# MongoDB ObjectID validation
def is_valid_mongo_id(value):
    return is_valid_regex(
        value,
        MONGO_ID_REGEX
    )


# Device name length validation
def is_valid_device_name_length(value):

    min_length = FIELD_LENGTHS[
        "deviceNameLength"
    ]["min"]

    max_length = FIELD_LENGTHS[
        "deviceNameLength"
    ]["max"]

    return validate_length(
        value,
        min_length,
        max_length
    )