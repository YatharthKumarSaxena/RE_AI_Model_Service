from src.services.get_embedding_service import (
    get_embedding_service
)

from src.responses.success.duplicate import (
    embedding_get_success
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


def get_embedding_controller(
    db,
    entity_id,
    entity_type
):
    try:

        embedding = get_embedding_service(
            db=db,
            entity_id=entity_id,
            entity_type=entity_type
        )

        log_with_time(
            "✅ [get_embedding_controller] "
            "Embedding fetched successfully"
        )

        return embedding_get_success({
            "entity_id": embedding.entity_id,
            "project_id": embedding.project_id,
            "entity_type": embedding.entity_type,
            "title": embedding.title,
            "description": embedding.description,
            "embedding": embedding.embedding
        })

    except Exception as error:

        log_with_time(
            "❌ [get_embedding_controller] "
            "Failed to fetch embedding"
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )