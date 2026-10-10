from src.configs.field_definitions import FieldDefinitions
from src.utils.field_definition import get_validation_set


validation_sets = {

    "convert_content_to_english_validation_set": get_validation_set(
        FieldDefinitions["CONVERT_CONTENT_TO_ENGLISH"]
    ),

    "import_entity_type_validation_set": get_validation_set(
        FieldDefinitions["IMPORT_ENTITY_TYPE"]
    ),

    "classify_entity_type_validation_set": get_validation_set(
        FieldDefinitions["CLASSIFY_ENTITY_TYPE"]
    ),

    "create_embedding_validation_set": get_validation_set(
        FieldDefinitions["CREATE_EMBEDDING"]
    ),

    "update_embedding_validation_set": get_validation_set(
        FieldDefinitions["UPDATE_EMBEDDING"]
    ),

    "force_update_embedding_validation_set": get_validation_set(
        FieldDefinitions["FORCE_UPDATE_EMBEDDING"]
    ),

    "get_embedding_validation_set": get_validation_set(
        FieldDefinitions["GET_EMBEDDING"]
    ),

    "list_embeddings_validation_set": get_validation_set(
        FieldDefinitions["LIST_EMBEDDINGS"]
    ),

    "delete_embedding_validation_set": get_validation_set(
        FieldDefinitions["DELETE_EMBEDDING"]
    )

}