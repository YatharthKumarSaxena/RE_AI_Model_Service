from flask import jsonify

from src.configs.http_status import OK
from src.utils.time_stamps import log_with_time


def dataset_success(data):

    log_with_time(
        "✅ [dataset_success] "
        "Dataset fetched successfully"
    )

    return jsonify({
        "success": True,
        "message": "Dataset fetched successfully",
        "data": data
    }), OK


def dataset_insights_success(data):

    log_with_time(
        "✅ [dataset_insights_success] "
        "Dataset insights fetched successfully"
    )

    return jsonify({
        "success": True,
        "message": "Dataset insights fetched successfully",
        "data": data
    }), OK