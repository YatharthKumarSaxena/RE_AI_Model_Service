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

            # ====================================================
            # GET IMPORT DATA
            # ====================================================

            import_data = getattr(
                request,
                "import_data",
                None
            )

            # Supports both:
            # request.import_data = {...}
            # request.import_data = [{...}, {...}]

            import_data_list = (
                import_data
                if isinstance(import_data, list)
                else [import_data]
            )

            # ====================================================
            # VALIDATE EACH IMPORT DATA
            # ====================================================

            for import_data_item in import_data_list:

                if not isinstance(
                    import_data_item,
                    dict
                ):
                    import_data_item = {}

                headers = import_data_item.get(
                    "headers",
                    []
                )

                result = validate_required_columns(
                    headers,
                    required_columns,
                    options
                )

                # =================================================
                # VALIDATION FAILED
                # =================================================

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
                            + ", ".join(
                                missing_columns
                            )
                        )

                    if duplicate_columns:

                        messages.append(
                            "Duplicate columns found: "
                            + ", ".join(
                                duplicate_columns
                            )
                        )

                    # ---------------------------------------------
                    # Cleanup uploaded files
                    # ---------------------------------------------

                    cleanup_uploaded_files(
                        file=getattr(
                            request,
                            "uploaded_file",
                            None
                        ),
                        files=getattr(
                            request,
                            "uploaded_files",
                            []
                        )
                    )

                    error_message = " ".join(
                        messages
                    )

                    log_middleware_error(
                        middleware_name,
                        error_message
                    )

                    return throw_bad_request_error(
                        error_message,
                        {
                            "missingColumns":
                                missing_columns,
                            "duplicateColumns":
                                duplicate_columns
                        }
                    )

                # =================================================
                # UPDATE CLEANED HEADERS
                # =================================================

                import_data_item["headers"] = (
                    result.get(
                        "cleanedHeaders",
                        []
                    )
                )

            # ====================================================
            # SUCCESS
            # ====================================================

            log_with_time(
                f"✅ [{middleware_name}] "
                "Required columns validation passed."
            )

            return None

        # ========================================================
        # UNEXPECTED ERROR
        # ========================================================

        except Exception as error:

            log_middleware_error(
                middleware_name,
                "Unexpected error while validating required columns."
            )

            cleanup_uploaded_files(
                file=getattr(
                    request,
                    "uploaded_file",
                    None
                ),
                files=getattr(
                    request,
                    "uploaded_files",
                    []
                )
            )

            return throw_internal_server_error(
                error
            )

    return middleware