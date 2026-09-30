from src.middlewares.factory.check_required_column_middleware_factory import (
    required_columns_check
)

from src.configs.required_fields import (
    required_fields
)


create_entity_type_field = required_fields[
    "import_entity_type_field"
]


validate_header_column_middlewares = {
    "create_entity_type_in_bulk_header_validation_middleware":
        required_columns_check(
            "createEntityTypeInBulkHeaderValidation",
            create_entity_type_field
        )
}