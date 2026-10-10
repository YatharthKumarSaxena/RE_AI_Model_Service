from src.services.embedding_service import (
    update_embedding_service
)

from src.responses.success.duplicate import (
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


def force_update_embedding_controller(
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

        update_embedding_service(
            db=db,
            project_id=project_id,
            entity_id=entity_id,
            entity_type=entity_type,
            title=title,
            description=description
        )

        log_with_time(
            "✅ [force_update_embedding_controller] "
            "Embedding force updated successfully"
        )

        return embedding_updated_success({
            "result": "FORCE_UPDATED",
            "entity_id": entity_id
        })

    except Exception as error:

        log_with_time(
            "❌ [force_update_embedding_controller] "
            "Failed to force update embedding"
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )