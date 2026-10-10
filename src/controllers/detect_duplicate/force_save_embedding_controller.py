from src.services.embedding_service import (
    save_embedding_service
)

from src.responses.success.duplicate import (
    duplicate_detection_success
)

from src.responses.common.error_handler import (
    throw_internal_server_error
)

from src.utils.time_stamps import (
    log_with_time
)

from src.utils.log_error import (
    error_message
)


def force_save_embedding_controller(
    db,
    project_id,
    entity_id,
    entity_type,
    title,
    description
):

    try:

        result = save_embedding_service(
            db=db,
            project_id=project_id,
            entity_id=entity_id,
            entity_type=entity_type,
            title=title,
            description=description
        )

        log_with_time(
            "✅ [force_save_embedding_controller] "
            "Embedding saved successfully"
        )

        return duplicate_detection_success({
            "result": "SAVED",
            "entity_id": entity_id
        })

    except Exception as error:

        log_with_time(
            "❌ [force_save_embedding_controller] "
            "Failed to save embedding"
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )