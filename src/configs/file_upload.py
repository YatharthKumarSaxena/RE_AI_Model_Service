import os
import time
import random

from src.utils.env import get_my_env_as_number
from src.utils.bulk_import_temp import TEMP_BASE


ENTITY_TYPE_IMPORT_FILE_CONFIG = {

    "upload_type": "array",

    "max_files": get_my_env_as_number(
        "ENTITY_TYPE_IMPORT_MAX_FILES",
        10
    ),

    "field_name": "file",

    "allowed_extensions": [
        ".xlsx",
        ".csv"
    ],

    "allowed_mime_types": [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/csv"
    ],

    "max_file_size_mb": get_my_env_as_number(
        "ENTITY_TYPE_IMPORT_MAX_FILE_SIZE_MB",
        20
    ),

    "destination": lambda request, file: os.path.join(
        TEMP_BASE,
        "_staging"
    ),

    "filename": lambda request, file: (
        f"chunk-{int(time.time() * 1000)}"
        f"-{random.randint(0, 10**9)}"
        f"{os.path.splitext(file.filename)[1].lower()}"
    )
}