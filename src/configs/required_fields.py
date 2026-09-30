from src.configs.field_definitions import FieldDefinitions
from src.utils.field_definition import (
    get_required_fields
)

required_fields = {
    "convert_content_to_english": get_required_fields(
        FieldDefinitions["CONVERT_CONTENT_TO_ENGLISH"]
    ),

    "import_entity_type_field": get_required_fields(
        FieldDefinitions["IMPORT_ENTITY_TYPE"]
    ),

    "classify_entity_type_field": get_required_fields(
        FieldDefinitions["CLASSIFY_ENTITY_TYPE"]
    )
}