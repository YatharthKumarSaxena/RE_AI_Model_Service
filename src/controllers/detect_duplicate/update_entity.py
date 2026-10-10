from src.services.duplicate_service import (
    check_duplicate_service
)

from src.services.update_embedding_service import (
    update_embedding_service
)

from src.responses.success.duplicate import (
    duplicate_detection_success,
    embedding_updated_success
)

from src.responses.common.error_handler import (
    throw_bad_request_error,
    throw_internal_server_error
)

from src.utils.time_stamps import (
    log_with_time
)

from src.utils.log_error import (
    error_message
)


def update_embedding_controller(
    db,
    project_id,
    entity_id,
    entity_type,
    title,
    description
):
    try:

        if not title and not description:
            return throw_bad_request_error(
                "Title or description is required"
            )
        
        result = check_duplicate_service(
            db=db,
            project_id=project_id,
            entity_id=entity_id,
            entity_type=entity_type,
            title=title,
            description=description
        )

        if result["result"] != "UNIQUE":

            result["embedding_updated"] = False

            log_with_time(
                "⚠️ [update_embedding_controller] "
                f"Duplicate detection result: "
                f"{result['result']}. "
                "Embedding not updated"
            )

            return duplicate_detection_success(
                result
            )

        update_embedding_service(
            db=db,
            project_id=project_id,
            entity_id=entity_id,
            entity_type=entity_type,
            title=title,
            description=description
        )

        result["embedding_updated"] = True

        log_with_time(
            "✅ [update_embedding_controller] "
            "Embedding updated successfully"
        )

        return embedding_updated_success({
            "result": "UPDATED",
            "entity_id": entity_id
        })

    except Exception as error:

        log_with_time(
            "❌ [update_embedding_controller] "
            "Embedding update failed"
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )