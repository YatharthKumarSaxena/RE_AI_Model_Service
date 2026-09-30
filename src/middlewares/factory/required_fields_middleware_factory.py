from flask import request

from src.utils.validate_fields import validate_missing_fields
from src.utils.time_stamps import log_with_time
from src.responses.common.error_handler import (
    log_middleware_error,
    throw_missing_fields_error,
    throw_internal_server_error
)


def _generic_presence_check(
    middleware_name,
    required_fields,
    request_location
):
    def middleware():
        try:
            # Flask request data
            if request_location == "body":
                data = request.get_json(silent=True) or {}

            elif request_location == "query":
                data = request.args.to_dict()

            elif request_location == "params":
                data = request.view_args or {}

            else:
                data = {}

            # Step 1: Utility Call
            result = validate_missing_fields(
                data,
                required_fields
            )

            # Step 2: Error Handling
            if not result["isValid"]:

                missing_fields = result.get(
                    "missingFields",
                    []
                )

                log_middleware_error(
                    middleware_name,
                    f"{request_location} missing fields: "
                    f"{', '.join(missing_fields)}"
                )

                return throw_missing_fields_error(
                    missing_fields
                )

            # Step 3: Cleaned / Trimmed data
            cleaned_data = result["cleanedData"]

            if request_location == "body":
                request.cleaned_body = cleaned_data

            elif request_location == "query":
                request.cleaned_query = cleaned_data

            elif request_location == "params":
                request.cleaned_params = cleaned_data

            log_with_time(
                f"✅ [{middleware_name}] "
                f"Required fields validation passed successfully "
                f"in {request_location}"
            )

            return None

        except Exception as error:

            log_middleware_error(
                middleware_name,
                f"Unexpected error in "
                f"{request_location} validation"
            )

            return throw_internal_server_error(error)

    return middleware


def check_body_presence(middleware_name, required_fields):
    return _generic_presence_check(
        middleware_name,
        required_fields,
        "body"
    )


def check_query_presence(middleware_name, required_fields):
    return _generic_presence_check(
        middleware_name,
        required_fields,
        "query"
    )


def check_params_presence(middleware_name, required_fields):
    return _generic_presence_check(
        middleware_name,
        required_fields,
        "params"
    )