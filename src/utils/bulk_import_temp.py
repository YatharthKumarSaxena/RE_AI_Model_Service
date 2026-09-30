import os

from src.utils.time_stamps import log_with_time


# ============================================================
# TEMP BASE DIRECTORY
# ============================================================

TEMP_BASE = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
    "uploads",
    "temp",
    "bulk-imports"
)


# ============================================================
# BULK IMPORT DIRECTORY
# ============================================================

def get_bulk_import_dir(bulk_import_id):

    return os.path.join(
        TEMP_BASE,
        str(bulk_import_id)
    )


# ============================================================
# PROCESSED FILE PATH
# ============================================================

def get_processed_file_path(bulk_import_id):

    return os.path.join(
        get_bulk_import_dir(bulk_import_id),
        "processed.xlsx"
    )


# ============================================================
# ORIGINAL FILE PATH
# ============================================================

def get_original_file_path(bulk_import_id):

    return os.path.join(
        get_bulk_import_dir(bulk_import_id),
        "original.xlsx"
    )


# ============================================================
# ENSURE BULK IMPORT DIRECTORY
# ============================================================

def ensure_bulk_import_dir(bulk_import_id):

    directory = get_bulk_import_dir(
        bulk_import_id
    )

    os.makedirs(
        directory,
        exist_ok=True
    )

    return directory


# ============================================================
# CLEANUP BULK IMPORT DIRECTORY
# ============================================================

def cleanup_bulk_import_dir(bulk_import_id):

    directory = get_bulk_import_dir(
        bulk_import_id
    )

    try:

        if os.path.exists(directory):

            # Remove entire directory recursively
            import shutil

            shutil.rmtree(
                directory
            )

        log_with_time(
            "🗑️ [bulkImportTempUtil] "
            f"Cleaned up temp dir for: {bulk_import_id}"
        )

    except Exception as error:

        log_with_time(
            "⚠️ [bulkImportTempUtil] "
            f"Failed to clean up {directory}: "
            f"{str(error)}"
        )


# ============================================================
# DELETE CHUNK FILE
# ============================================================

def delete_chunk_file(file_path):

    try:

        if file_path and os.path.exists(file_path):

            os.remove(
                file_path
            )

    except Exception as error:

        log_with_time(
            "⚠️ [bulkImportTempUtil] "
            f"Failed to delete chunk "
            f"{file_path}: {str(error)}"
        )


# ============================================================
# DELETE FILE IF EXISTS
# ============================================================

def delete_file_if_exists(file_path):

    try:

        if file_path and os.path.exists(file_path):

            os.remove(
                file_path
            )

    except Exception as error:

        log_with_time(
            "⚠️ [bulkImportTempUtil] "
            f"Failed to delete file "
            f"{file_path}: {str(error)}"
        )


# ============================================================
# CLEANUP UPLOADED FILES
# ============================================================

def cleanup_uploaded_files(
    file=None,
    files=None
):

    # --------------------------------------------------------
    # Single file
    # --------------------------------------------------------

    if file:

        file_path = (
            file.get("path")
            if isinstance(file, dict)
            else getattr(file, "path", None)
        )

        delete_file_if_exists(
            file_path
        )

    # --------------------------------------------------------
    # Multiple files
    # --------------------------------------------------------

    if isinstance(files, list):

        for uploaded_file in files:

            file_path = (
                uploaded_file.get("path")
                if isinstance(uploaded_file, dict)
                else getattr(
                    uploaded_file,
                    "path",
                    None
                )
            )

            delete_file_if_exists(
                file_path
            )