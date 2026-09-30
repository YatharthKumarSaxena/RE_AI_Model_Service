from src.utils.validators_factory import (
    is_valid_enum_value,
    get_enum_key_by_value
)

from src.utils.time_stamps import log_with_time

from src.configs.enums import (
    ProjectTypes,
    RequestLocation,
    EntityTypeModel,
    DeviceType
)

# ============================================================
# ENUM HELPER FACTORY
# ============================================================

def create_enum_helper(enum_class, name):

    def validate(value):
        result = is_valid_enum_value(
            enum_class,
            value
        )

        log_with_time(
            f'[{name}] validate("{value}") → {result}'
        )

        return result

    def reverse_lookup(value):
        result = get_enum_key_by_value(
            enum_class,
            value
        )

        log_with_time(
            f'[{name}] reverseLookup("{value}") → {result}'
        )

        return result

    def get_valid_values():
        return [
            enum.value
            for enum in enum_class
        ]

    def get_name():
        return name

    return {
        "validate": validate,
        "reverse_lookup": reverse_lookup,
        "get_valid_values": get_valid_values,
        "get_name": get_name,
        "enum_class": enum_class
    }


# ============================================================
# ENUM-SPECIFIC HELPERS
# ============================================================

ProjectTypesHelper = create_enum_helper(
    ProjectTypes,
    "ProjectTypes"
)

RequestLocationHelper = create_enum_helper(
    RequestLocation,
    "RequestLocation"
)

EntityTypeModelHelper = create_enum_helper(
    EntityTypeModel,
    "EntityTypeModel"
)

DeviceTypeHelper = create_enum_helper(
    DeviceType,
    "DeviceType"
)