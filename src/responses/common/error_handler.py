import json

from flask import jsonify

from src.utils.time_stamps import log_with_time
from src.configs.http_status import (
    BAD_REQUEST,
    INTERNAL_ERROR,
    UNAUTHORIZED,
    FORBIDDEN,
    CONFLICT,
    UNPROCESSABLE_ENTITY,
    NOT_FOUND,
    TOO_MANY_REQUESTS
)
from src.utils.log_error import (
    error_message,
    log_middleware_error
)


def throw_missing_fields_error(resource):
    log_with_time("⚠️ Missing required fields in the request:")
    print(resource)

    return jsonify({
        "success": False,
        "warning": "The following required field(s) are missing:",
        "fields": resource,
        "message": "Please provide the required fields to proceed."
    }), BAD_REQUEST


def throw_invalid_resource_error(resource, reason):
    log_with_time(f"⚠️ Invalid {resource}")
    log_with_time("❌ Invalid Credentials! Please try again.")

    return jsonify({
        "success": False,
        "type": "InvalidResource",
        "resource": resource,
        "reason": reason,
        "warning": f"Invalid {resource} Entered",
        "message": f"Please enter a Valid {resource}"
    }), UNAUTHORIZED


def throw_access_denied_error(reason="Access Denied"):
    log_with_time(f"⛔️ Access Denied: {reason}")

    return jsonify({
        "success": False,
        "type": "AccessDenied",
        "warning": reason,
        "message": "You do not have the necessary permissions to perform this action."
    }), FORBIDDEN


def throw_bad_request_error(reason="Bad Request", details=None):
    log_with_time(f"⚠️ Bad Request: {reason}")

    return jsonify({
        "success": False,
        "type": "BadRequest",
        "warning": reason,
        "details": details,
        "message": "The request could not be processed due to invalid or missing data."
    }), BAD_REQUEST


def throw_conflict_error(message, suggestion):
    log_with_time(f"⚔️ Conflict Detected: {message}")

    return jsonify({
        "success": False,
        "message": message,
        "suggestion": suggestion
    }), CONFLICT


def throw_db_resource_not_found_error(resource):
    log_with_time(f"⚠️ Resource Not Found in Database: {resource}")

    return jsonify({
        "success": False,
        "type": "ResourceNotFound",
        "resource": resource,
        "warning": f"{resource} not found.",
        "message": (
            f"The specified {resource} does not exist. "
            "Please verify and try again."
        )
    }), NOT_FOUND


def throw_session_expired_error(reason="Session expired"):
    log_with_time(f"⏳ Session Expired: {reason}")

    return jsonify({
        "success": False,
        "type": "SessionExpired",
        "warning": reason,
        "message": "Your session has expired. Please login again to continue."
    }), UNAUTHORIZED


def throw_validation_error(errors):
    log_with_time(f"⚠️ Validation Error: {json.dumps(errors)}")

    return jsonify({
        "success": False,
        "type": "ValidationError",
        "errors": errors,
        "message": (
            "The request contains invalid data. "
            "Please review the errors and try again."
        )
    }), UNPROCESSABLE_ENTITY


def throw_internal_server_error(error):
    if getattr(error, "name", None) == "ValidationError":
        log_with_time(f"⚠️ Validation Error: {str(error)}")
        return throw_bad_request_error(str(error))

    error_message(error)

    log_with_time("💥 Internal Server Error occurred.")

    return jsonify({
        "success": False,
        "response": (
            "An internal server error occurred "
            "while processing your request."
        ),
        "message": (
            "We apologize for the inconvenience. "
            "Please try again later."
        )
    }), INTERNAL_ERROR


def throw_specific_internal_server_error(custom_message):
    log_with_time(f"💥 Internal Server Error: {custom_message}")

    return jsonify({
        "success": False,
        "response": (
            "An internal server error occurred "
            "while processing your request."
        ),
        "message": custom_message
    }), INTERNAL_ERROR


def throw_too_many_requests_error(message, retry_after=None):
    log_with_time(f"⏳ Too Many Requests: {message}")

    response = {
        "success": False,
        "type": "TooManyRequests",
        "warning": "Rate Limit Exceeded",
        "message": (
            message
            or "You have exceeded the maximum number of requests. "
               "Please try again later."
        )
    }

    if retry_after:
        response["retryAfterSeconds"] = retry_after

    return jsonify(response), TOO_MANY_REQUESTS


def throw_feature_disabled_error(
    feature_name,
    reason="This feature is currently disabled."
):
    log_with_time(
        f"🚫 Feature Disabled: {feature_name} - {reason}"
    )

    return jsonify({
        "success": False,
        "type": "FeatureDisabled",
        "feature": feature_name,
        "warning": reason,
        "message": (
            f"{feature_name} is not available based on "
            "current system configuration."
        )
    }), FORBIDDEN


def throw_unauthorized_error(resource, reason):
    log_with_time(f"⚠️ Invalid {resource}")
    log_with_time("❌ Invalid Credentials! Please try again.")

    return jsonify({
        "success": False,
        "type": "Unauthorized",
        "resource": resource,
        "reason": reason,
        "warning": f"Invalid {resource} Entered",
        "message": f"Please enter a Valid {resource}"
    }), UNAUTHORIZED