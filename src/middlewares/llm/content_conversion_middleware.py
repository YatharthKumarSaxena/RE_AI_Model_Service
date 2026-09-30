from flask import request

from src.services.llm_service import (
    process_text
)
from src.responses.common.error_handler import (
    throw_bad_request_error,
    throw_internal_server_error
)
from src.utils.time_stamps import log_with_time
from src.utils.log_error import error_message


def convert_content_to_english_middleware():
    try:
        raw_data = request.get_json()

        raw_title = raw_data.get("rawTitle")
        raw_description = raw_data.get("rawDescription")

        result = process_text(
            raw_title,
            raw_description
        )

        if not result:
            log_with_time(
                "❌ [convertContentToEnglishMiddleware] "
                "English conversion failed"
            )

            return throw_internal_server_error(
                "Failed to convert content to English."
            )

        # AI could not understand the provided content
        if result.get("need_clarification") is True:

            log_with_time(
                "⚠️ [convertContentToEnglishMiddleware] "
                "Content is unclear or not meaningful"
            )

            return throw_bad_request_error(
                "The provided raw title and description are unclear "
                "or not meaningful. Please provide clear and meaningful "
                "content.",
                {
                    "needClarification": True
                }
            )

        # Store converted content for controller
        request.converted_content = {
            "title": result.get("title"),
            "description": result.get("description"),
            "need_clarification": result.get("need_clarification")
        }

        log_with_time(
            "✅ [convertContentToEnglishMiddleware] "
            "Content converted successfully"
        )

        return None

    except Exception as error:
        log_with_time(
            "❌ [convertContentToEnglishMiddleware] "
            f"Unexpected error: {str(error)}"
        )

        error_message(error)

        return throw_internal_server_error(error)