from src.configs.file_upload import (
    ENTITY_TYPE_IMPORT_FILE_CONFIG
)

from src.middlewares.factory.file_upload_middleware_factory import (
    create_file_upload_middleware
)


file_upload_middlewares = {
    "check_entity_type_import_file_upload_configuration":
        create_file_upload_middleware(
            middleware_name="checkEntityTypeImportFileConfiguration",
            **ENTITY_TYPE_IMPORT_FILE_CONFIG
        )
}