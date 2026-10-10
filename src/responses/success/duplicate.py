from flask import jsonify

from src.configs.http_status import OK
from src.utils.time_stamps import log_with_time


def embedding_saved_success(data):

    log_with_time(
        "✅ [embedding_saved_success] "
        "Embedding saved successfully"
    )

    return jsonify({
        "success": True,
        "message": "Embedding saved successfully",
        "data": data
    }), OK


def duplicate_detection_success(data):

    log_with_time(
        "✅ [duplicate_detection_success] "
        "Duplicate detection completed successfully"
    )

    return jsonify({
        "success": True,
        "message": "Duplicate detection completed successfully",
        "data": data
    }), OK


def embedding_updated_success(data):
    log_with_time(
        "✅ [embedding_updated_success] "
        "Embedding updated successfully"
    )

    return jsonify({
        "success": True,
        "message": "Embedding updated successfully",
        "data": data
    }), OK


def embedding_deleted_success(data):
    log_with_time(
        "✅ [embedding_deleted_success] "
        "Embedding deleted successfully"
    )

    return jsonify({
        "success": True,
        "message": "Embedding deleted successfully",
        "data": data
    }), OK

def embedding_get_success(data):
    log_with_time(
        "✅ [embedding_get_success] "
        "Embedding fetched successfully"
    )

    return jsonify({
        "success": True,
        "message": "Embedding fetched successfully",
        "data": data
    }), OK

def embedding_list_success(data):
    log_with_time(
        "✅ [embedding_list_success] "
        "Embeddings fetched successfully"
    )

    return jsonify({
        "success": True,
        "message": "Embeddings fetched successfully",
        "data": data
    }), OK