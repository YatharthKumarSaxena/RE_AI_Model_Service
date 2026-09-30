from flask import jsonify

from src.configs.http_status import OK
from src.utils.time_stamps import log_with_time


def content_english_conversion_success(result):
    log_with_time(
        "✅ [content_english_conversion_success] "
        "Content converted to English successfully"
    )

    return jsonify({
        "success": True,
        "message": "Content converted to English successfully",
        "data": {
            "title": result.get("title"),
            "description": result.get("description"),
            "need_clarification": result.get("need_clarification")
        }
    }), OK