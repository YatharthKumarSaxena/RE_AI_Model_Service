from flask import request

from src.services.llm_service import process_text
from src.responses.common.error_handler import (
    throw_bad_request_error,
    throw_internal_server_error,
    throw_specific_internal_server_error
)
from src.responses.success.llm import (
    content_english_conversion_success
)
from src.utils.time_stamps import log_with_time
from src.utils.log_error import error_message


def convert_content_to_english_controller():
    try:
        data = request.get_json()

        if not data:
            log_with_time(
                "❌ [convertContentToEnglishController] Request body is missing"
            )
            return throw_bad_request_error(
                "Request body is required."
            )

        raw_title = data.get(
            "rawTitle",
            ""
        ) or ""

        raw_description = data.get(
            "rawDescription",
            ""
        ) or ""

        result = process_text(
            raw_title,
            raw_description
        )

        if not result:
            log_with_time(
                "❌ [convertContentToEnglishController] "
                "English conversion failed"
            )
            return throw_specific_internal_server_error(
                "Failed to convert content to English."
            )

        log_with_time(
            "✅ [convertContentToEnglishController] "
            "Content converted to English successfully"
        )

        return content_english_conversion_success(result)

    except Exception as error:
        log_with_time(
            f"❌ [convertContentToEnglishController] "
            f"Unexpected error: {str(error)}"
        )

        error_message(error)

        return throw_internal_server_error(error)