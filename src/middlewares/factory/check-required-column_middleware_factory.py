from flask import request

from src.utils.validate_fields import validate_required_columns
from src.responses.common.error_handler import (
    throw_internal_server_error,
    log_middleware_error,
    throw_bad_request_error
)

from src.utils.time_stamps import log_with_time
from src.utils.bulk_import_temp import cleanup_uploaded_files


def required_columns_check(
    middleware_name,
    required_columns,
    options=None
):
    if options is None:
        options = {}

    def middleware():

        try:

            # Supports both:
            # request.import_data = {...}
            # request.import_data = [{...}, {...}]

            import_data = getattr(
                request,
                "import_data",
                None
            )

            import_data_list = (
                import_data
                if isinstance(import_data, list)
                else [import_data]
            )

            for data in import_data_list:

                headers = (
                    data.get("headers", [])
                    if isinstance(data, dict)
                    else []
                )

                result = validate_required_columns(
                    headers,
                    required_columns,
                    options
                )

                if not result["isValid"]:

                    messages = []

                    missing_columns = result.get(
                        "missingColumns",
                        []
                    )

                    duplicate_columns = result.get(
                        "duplicateColumns",
                        []
                    )

                    if missing_columns:
                        messages.append(
                            "Missing required columns: "
                            + ", ".join(missing_columns)
                        )

                    if duplicate_columns:
                        messages.append(
                            "Duplicate columns found: "
                            + ", ".join(duplicate_columns)
                        )

                    cleanup_uploaded_files(
                        file=request.files.get("file"),
                        files=request.files
                    )

                    error_text = " ".join(messages)

                    log_middleware_error(
                        middleware_name,
                        error_text
                    )

                    return throw_bad_request_error(
                        error_text,
                        {
                            "missingColumns": missing_columns,
                            "duplicateColumns": duplicate_columns
                        }
                    )

                # Replace headers with cleaned headers
                if isinstance(data, dict):
                    data["headers"] = result.get(
                        "cleanedHeaders",
                        []
                    )

            log_with_time(
                f"✅ [{middleware_name}] "
                "Required columns validation passed."
            )

            return None

        except Exception as error:

            log_middleware_error(
                middleware_name,
                "Unexpected error while validating required columns."
            )

            cleanup_uploaded_files(
                file=request.files.get("file"),
                files=request.files
            )

            return throw_internal_server_error(error)

    return middleware