from src.services.delete_embedding_service import (
    delete_embedding_service
)

from src.responses.success.duplicate import (
    embedding_deleted_success
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


def delete_embedding_controller(
    db,
    entity_id,
    entity_type
):
    try:

        delete_embedding_service(
            db=db,
            entity_id=entity_id,
            entity_type=entity_type
        )

        log_with_time(
            "✅ [delete_embedding_controller] "
            "Embedding deleted successfully"
        )

        return embedding_deleted_success({
            "result": "DELETED",
            "entity_id": entity_id
        })

    except Exception as error:

        log_with_time(
            "❌ [delete_embedding_controller] "
            "Embedding deletion failed"
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )