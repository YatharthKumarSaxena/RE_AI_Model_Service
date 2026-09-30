from flask import request

from src.utils.validators_factory import (
    is_valid_regex,
    validate_length
)

from src.utils.time_stamps import log_with_time

from src.responses.common.error_handler import (
    throw_internal_server_error,
    log_middleware_error,
    throw_validation_error
)


def _generic_validation(
    controller_name,
    validation_set,
    request_location
):
    def middleware():

        try:
            fields_to_validate = validation_set

            # Request data
            if request_location == "body":
                data = request.get_json(silent=True) or {}

            elif request_location == "query":
                data = request.args.to_dict()

            elif request_location == "params":
                data = request.view_args or {}

            else:
                log_middleware_error(
                    controller_name,
                    f"Invalid request location: {request_location}"
                )

                return throw_internal_server_error(
                    Exception("Invalid validation location")
                )

            # Validation set check
            if not fields_to_validate:

                log_middleware_error(
                    controller_name,
                    "No validation set provided"
                )

                return throw_internal_server_error(
                    Exception("Validation set is required")
                )

            errors = []

            # Iterate over validation rules
            for field, rules in fields_to_validate.items():

                value = data.get(field)

                # Optional Field Handling
                if value is None:
                    continue

                if rules.get("enum"):

                    enum = rules["enum"]

                    is_valid = enum["validate"](value)

                    if not is_valid:

                        valid_values = ", ".join(
                            enum["get_valid_values"]()
                        )

                        errors.append({
                            "field": field,
                            "message": (
                                f"{field} must be one of: "
                                f"{valid_values}"
                            ),
                            "received": value
                        })

                    continue

                # Regex Validation
                regex = rules.get("regex")

                if regex and not is_valid_regex(value, regex):

                    errors.append({
                        "field": field,
                        "message": f"{field} format is invalid",
                        "received": value
                    })

                # Length Validation
                length = rules.get("length")

                if length:

                    min_length = length.get("min")
                    max_length = length.get("max")

                    is_valid = validate_length(
                        value,
                        min_length,
                        max_length
                    )

                    if not is_valid:

                        if min_length == max_length:

                            message = (
                                f"Length must be exactly "
                                f"{min_length} characters."
                            )

                        else:

                            message = (
                                f"Length must be between "
                                f"{min_length} and "
                                f"{max_length} characters."
                            )

                        errors.append({
                            "field": field,
                            "message": message,
                            "received": value
                        })

            # Validation failed
            if errors:

                log_middleware_error(
                    controller_name,
                    f"Validation failed in {request_location}"
                )

                return throw_validation_error(
                    errors
                )


            # Success
            log_with_time(
                f"✅ [{controller_name}] "
                f"Validation passed successfully in {request_location}"
            )
            return None

        except Exception as error:

            log_middleware_error(
                controller_name,
                f"Middleware error in {request_location}"
            )

            return throw_internal_server_error(error)

    return middleware


# --------------------------------------------------
# 1. Validate Body
# --------------------------------------------------

def validate_body(controller_name, validation_set):

    return _generic_validation(
        controller_name,
        validation_set,
        "body"
    )


# --------------------------------------------------
# 2. Validate Query
# --------------------------------------------------

def validate_query(controller_name, validation_set):

    return _generic_validation(
        controller_name,
        validation_set,
        "query"
    )


# --------------------------------------------------
# 3. Validate Route Params
# --------------------------------------------------

def validate_params(controller_name, validation_set):

    return _generic_validation(
        controller_name,
        validation_set,
        "params"
    )