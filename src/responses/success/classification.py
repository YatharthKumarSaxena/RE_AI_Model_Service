from flask import jsonify

from src.configs.http_status import OK
from src.utils.time_stamps import log_with_time


def entity_type_bulk_import_success(result):

    log_with_time(
        "✅ [entity_type_bulk_import_success] "
        "Entity type bulk import processed successfully"
    )

    return jsonify({
        "success": True,
        "message": (
            "Entity type bulk import processed successfully"
        ),
        "data": {
            "totalRows": result.get("totalRows", 0),
            "validRows": result.get("validRows", 0),
            "invalidRows": result.get("invalidRows", 0),
            "rows": result.get("rows", [])
        }
    }), OK


from flask import jsonify

from src.configs.http_status import OK
from src.utils.time_stamps import log_with_time


def entity_type_bulk_import_success(result):

    log_with_time(
        "✅ [entity_type_bulk_import_success] "
        "Entity type bulk import processed successfully"
    )

    return jsonify({
        "success": True,
        "message": (
            "Entity type bulk import processed successfully"
        ),
        "data": {
            "totalRows": result.get("totalRows", 0),
            "validRows": result.get("validRows", 0),
            "invalidRows": result.get("invalidRows", 0),
            "rows": result.get("rows", [])
        }
    }), OK


def entity_type_classification_success(
    title,
    description,
    classification_result
):

    log_with_time(
        "✅ [entity_type_classification_success] "
        "Entity type classification completed successfully"
    )

    return jsonify({
        "success": True,
        "message": "Entity type classified successfully",
        "data": {
            "title": title,
            "description": description,
            "entityType": classification_result.get(
                "prediction"
            ),
            "score": classification_result.get(
                "score"
            ),
            "scoreType": classification_result.get(
                "score_type"
            ),
            "classScores": classification_result.get(
                "class_scores",
                {}
            )
        }
    }), OK