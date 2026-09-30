import os
from flask import request

from src.responses.common.error_handler import (
    throw_bad_request_error,
    throw_internal_server_error,
    log_middleware_error
)

from src.utils.time_stamps import log_with_time
from src.utils.bulk_import_temp import cleanup_uploaded_files


def create_parse_file_middleware(
    middleware_name="Parse File",
    parsers=None
):

    if parsers is None:
        parsers = []

    def middleware():

        try:

            # ====================================================
            # GET UPLOADED FILES
            # ====================================================

            uploaded_file = getattr(
                request,
                "uploaded_file",
                None
            )

            uploaded_files = getattr(
                request,
                "uploaded_files",
                []
            )

            if uploaded_file:
                files = [uploaded_file]
            else:
                files = uploaded_files or []

            # ====================================================
            # NO FILE CHECK
            # ====================================================

            if not files:

                log_middleware_error(
                    middleware_name,
                    "No uploaded files found."
                )

                return throw_bad_request_error(
                    "No uploaded files found."
                )

            # ====================================================
            # PARSE FILES
            # ====================================================

            parsed_data = []

            for file_info in files:

                # ------------------------------------------------
                # Get file path
                # ------------------------------------------------

                file_path = file_info.get("path")

                original_name = file_info.get(
                    "originalname",
                    ""
                )

                if not file_path:

                    log_middleware_error(
                        middleware_name,
                        "Uploaded file path is missing."
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

                    return throw_bad_request_error(
                        "Uploaded file path is missing."
                    )

                # ------------------------------------------------
                # Get extension
                # ------------------------------------------------

                extension = os.path.splitext(
                    original_name
                )[1].lower()

                parser_found = False

                # =================================================
                # FIND PARSER
                # =================================================

                for parser in parsers:

                    supported_extensions = parser.get(
                        "supported_extensions"
                    )

                    if (
                        supported_extensions
                        and extension not in supported_extensions
                    ):
                        continue

                    parser_found = True

                    # ------------------------------------------------
                    # Execute parser
                    # ------------------------------------------------

                    try:

                        result = parser["parse"](
                            file_path,
                            extension
                        )

                    except Exception as error:

                        log_middleware_error(
                            middleware_name,
                            str(error)
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

                        return throw_bad_request_error(
                            str(error)
                        )

                    # ------------------------------------------------
                    # Parser failure
                    # ------------------------------------------------

                    if not result.get("success"):

                        reason = result.get(
                            "reason",
                            "Failed to parse file."
                        )

                        log_middleware_error(
                            middleware_name,
                            reason
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

                        return throw_bad_request_error(
                            reason
                        )

                    # ------------------------------------------------
                    # Store parsed data
                    # ------------------------------------------------

                    parsed_data.append(
                        result.get("data")
                    )

                    log_with_time(
                        f"✅ [{middleware_name}] "
                        f"'{original_name}' parsed successfully "
                        f"using '{parser.get('name', 'Unknown')}'."
                    )

                    break

                # =================================================
                # NO PARSER FOUND
                # =================================================

                if not parser_found:

                    message = (
                        f"Unsupported file format "
                        f"'{extension}'."
                    )

                    log_middleware_error(
                        middleware_name,
                        f"No parser found for '{extension}'."
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

                    return throw_bad_request_error(
                        message
                    )

            # ====================================================
            # STORE IMPORT DATA
            # ====================================================

            request.import_data = (
                parsed_data[0]
                if len(parsed_data) == 1
                else parsed_data
            )

            return None

        except Exception as error:

            log_middleware_error(
                middleware_name,
                "Unexpected error while parsing file."
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