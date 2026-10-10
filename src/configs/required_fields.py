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
    ),

    "create_embedding_field": get_required_fields(
        FieldDefinitions["CREATE_EMBEDDING"]
    ),

    "update_embedding_field": get_required_fields(
        FieldDefinitions["UPDATE_EMBEDDING"]
    ),

    "force_update_embedding_field": get_required_fields(
        FieldDefinitions["FORCE_UPDATE_EMBEDDING"]
    ),

    "get_embedding_field": get_required_fields(
        FieldDefinitions["GET_EMBEDDING"]
    ),

    "list_embeddings_field": get_required_fields(
        FieldDefinitions["LIST_EMBEDDINGS"]
    ),

    "delete_embedding_field": get_required_fields(
        FieldDefinitions["DELETE_EMBEDDING"]
    )

}