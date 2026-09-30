from flask import jsonify

from src.configs.http_status import OK

from src.utils.time_stamps import (
    log_with_time
)


def model_evaluation_success(data):

    log_with_time(
        "✅ [model_evaluation_success] "
        "Model evaluation data fetched successfully"
    )

    return jsonify({
        "success": True,
        "message": "Model evaluation data fetched successfully",
        "data": data
    }), OK