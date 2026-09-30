import os
from functools import wraps
from flask import request

from src.responses.common.error_handler import (
    throw_bad_request_error,
    throw_internal_server_error,
    log_middleware_error
)

from src.utils.time_stamps import log_with_time
from src.utils.bulk_import_temp import cleanup_uploaded_files


def create_file_upload_middleware(
    middleware_name="File Upload",
    upload_type="single",
    field_name="file",
    max_files=1,
    allowed_extensions=None,
    allowed_mime_types=None,
    max_file_size_mb=20,
    destination=None,
    filename=None
):

    if allowed_extensions is None:
        allowed_extensions = []

    if allowed_mime_types is None:
        allowed_mime_types = []

    # ============================================================
    # CONFIG VALIDATION
    # ============================================================

    if upload_type not in ["single", "array"]:
        raise ValueError(
            f"[{middleware_name}] "
            "upload_type must be 'single' or 'array'."
        )

    if not isinstance(max_files, int) or max_files <= 0:
        raise ValueError(
            f"[{middleware_name}] "
            "max_files must be a positive integer."
        )

    if not callable(destination):
        raise ValueError(
            f"[{middleware_name}] "
            "destination must be a function."
        )

    if not callable(filename):
        raise ValueError(
            f"[{middleware_name}] "
            "filename must be a function."
        )

    if not isinstance(allowed_extensions, list):
        raise ValueError(
            f"[{middleware_name}] "
            "allowed_extensions must be a list."
        )

    if not isinstance(allowed_mime_types, list):
        raise ValueError(
            f"[{middleware_name}] "
            "allowed_mime_types must be a list."
        )

    if (
        not isinstance(max_file_size_mb, (int, float))
        or max_file_size_mb <= 0
    ):
        raise ValueError(
            f"[{middleware_name}] "
            "max_file_size_mb must be a positive number."
        )

    max_file_size_bytes = (
        max_file_size_mb * 1024 * 1024
    )

    # ============================================================
    # MIDDLEWARE
    # ============================================================

    def middleware():

        try:

            # ----------------------------------------------------
            # GET UPLOADED FILES
            # ----------------------------------------------------

            if upload_type == "single":

                uploaded_file = request.files.get(
                    field_name
                )

                files = (
                    [uploaded_file]
                    if uploaded_file
                    else []
                )

            else:

                files = request.files.getlist(
                    field_name
                )

                uploaded_file = (
                    files[0]
                    if files
                    else None
                )

            # ----------------------------------------------------
            # CHECK FILE EXISTENCE
            # ----------------------------------------------------

            if not files:

                log_middleware_error(
                    middleware_name,
                    (
                        "No file uploaded. "
                        f"Field name must be '{field_name}'."
                    )
                )

                message = (
                    f"No file uploaded. "
                    f"Field name must be '{field_name}'."
                    if upload_type == "single"
                    else
                    f"No files uploaded. "
                    f"Field name must be '{field_name}'."
                )

                return throw_bad_request_error(
                    message
                )

            # ----------------------------------------------------
            # CHECK FILE COUNT
            # ----------------------------------------------------

            if len(files) > max_files:

                cleanup_uploaded_files(
                    file=uploaded_file,
                    files=files
                )

                message = (
                    f"Maximum {max_files} file(s) are allowed."
                )

                log_middleware_error(
                    middleware_name,
                    message
                )

                return throw_bad_request_error(
                    message
                )

            # ----------------------------------------------------
            # VALIDATE EACH FILE
            # ----------------------------------------------------

            for file in files:

                if not file or not file.filename:

                    cleanup_uploaded_files(
                        file=uploaded_file,
                        files=files
                    )

                    message = (
                        f"No file uploaded. "
                        f"Field name must be '{field_name}'."
                    )

                    log_middleware_error(
                        middleware_name,
                        message
                    )

                    return throw_bad_request_error(
                        message
                    )

                # ------------------------------------------------
                # FILE SIZE
                # ------------------------------------------------

                file.stream.seek(
                    0,
                    os.SEEK_END
                )

                file_size = file.stream.tell()

                file.stream.seek(0)

                if file_size > max_file_size_bytes:

                    cleanup_uploaded_files(
                        file=uploaded_file,
                        files=files
                    )

                    message = (
                        f"Maximum allowed file size is "
                        f"{max_file_size_mb} MB."
                    )

                    log_middleware_error(
                        middleware_name,
                        message
                    )

                    return throw_bad_request_error(
                        message
                    )

                # ------------------------------------------------
                # FILE EXTENSION
                # ------------------------------------------------

                extension = os.path.splitext(
                    file.filename
                )[1].lower()

                normalized_extensions = [
                    ext.lower()
                    for ext in allowed_extensions
                ]

                if (
                    normalized_extensions
                    and extension not in normalized_extensions
                ):

                    cleanup_uploaded_files(
                        file=uploaded_file,
                        files=files
                    )

                    message = (
                        f"Invalid file extension "
                        f"'{extension}'. Allowed: "
                        f"{', '.join(allowed_extensions)}"
                    )

                    log_middleware_error(
                        middleware_name,
                        message
                    )

                    return throw_bad_request_error(
                        message
                    )

                # ------------------------------------------------
                # MIME TYPE
                # ------------------------------------------------

                if (
                    allowed_mime_types
                    and file.mimetype not in allowed_mime_types
                ):

                    cleanup_uploaded_files(
                        file=uploaded_file,
                        files=files
                    )

                    message = (
                        f"Invalid MIME type "
                        f"'{file.mimetype}'."
                    )

                    log_middleware_error(
                        middleware_name,
                        message
                    )

                    return throw_bad_request_error(
                        message
                    )

            # ====================================================
            # SAVE FILES
            # ====================================================

            saved_files = []

            for file in files:

                try:

                    upload_path = destination(
                        request,
                        file
                    )

                    os.makedirs(
                        upload_path,
                        exist_ok=True
                    )

                    generated_filename = filename(
                        request,
                        file
                    )

                    file_path = os.path.join(
                        upload_path,
                        generated_filename
                    )

                    file.save(file_path)

                    saved_files.append({
                        "file": file,
                        "path": file_path,
                        "filename": generated_filename,
                        "originalname": file.filename,
                        "mimetype": file.mimetype,
                        "size": os.path.getsize(file_path)
                    })

                except Exception as error:

                    cleanup_uploaded_files(
                        file=uploaded_file,
                        files=files
                    )

                    log_middleware_error(
                        middleware_name,
                        str(error)
                    )

                    return throw_internal_server_error(
                        error
                    )

            # ====================================================
            # STORE FILE INFORMATION
            # ====================================================

            if upload_type == "single":

                request.uploaded_file = (
                    saved_files[0]
                )

            else:

                request.uploaded_files = (
                    saved_files
                )

            # ====================================================
            # SUCCESS LOG
            # ====================================================

            log_with_time(
                f"✅ {middleware_name}: "
                f"{'File' if upload_type == 'single' else f'{len(files)} file(s)'} "
                "uploaded successfully."
            )

            return None

        except Exception as error:

            log_middleware_error(
                middleware_name,
                str(error)
            )

            cleanup_uploaded_files(
                file=request.files.get(field_name),
                files=request.files.getlist(field_name)
            )

            return throw_internal_server_error(
                error
            )

    return middleware