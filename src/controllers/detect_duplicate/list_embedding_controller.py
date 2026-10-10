from src.services.list_embedding_service import (
    list_embedding_service
)

from src.responses.success.duplicate import (
    embedding_list_success
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


def list_embedding_controller(
    db,
    project_id,
    entity_type=None,
    page=1,
    limit=20
):
    try:

        # ─── Pagination Validation ───────────────────────────────

        if page < 1:
            page = 1

        if limit < 1:
            limit = 1
        elif limit > 100:
            limit = 100

        # ─── Fetch Embeddings ────────────────────────────────────

        embeddings = list_embedding_service(
            db=db,
            project_id=project_id,
            entity_type=entity_type,
            page=page,
            limit=limit
        )

        data = []

        for embedding in embeddings:

            data.append({
                "entity_id": embedding.entity_id,
                "project_id": embedding.project_id,
                "entity_type": embedding.entity_type,
                "title": embedding.title,
                "description": embedding.description
            })

        log_with_time(
            "✅ [list_embedding_controller] "
            f"Embeddings fetched successfully: "
            f"{len(data)}"
        )

        return embedding_list_success(data)

    except Exception as error:

        log_with_time(
            "❌ [list_embedding_controller] "
            "Failed to fetch embeddings"
        )

        error_message(error)

        return throw_internal_server_error(error)