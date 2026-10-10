from src.services.duplicate_service import (
    check_duplicate_service
)

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


def check_duplicate_controller(
    db,
    project_id,
    entity_id,
    entity_type,
    title,
    description
):

    try:

        # Step 1: Check for duplicates
        result = check_duplicate_service(
            db=db,
            project_id=project_id,
            entity_id=entity_id,
            entity_type=entity_type,
            title=title,
            description=description
        )

        # Step 2: Save only when no match is found
        if result["result"] == "UNIQUE":

            save_embedding_service(
                db=db,
                project_id=project_id,
                entity_id=entity_id,
                entity_type=entity_type,
                title=title,
                description=description
            )

            log_with_time(
                "✅ [check_duplicate_controller] "
                "No duplicate found. "
                "Embedding saved successfully"
            )

            result["embedding_saved"] = True

        else:

            result["embedding_saved"] = False

            log_with_time(
                "⚠️ [check_duplicate_controller] "
                f"Duplicate detection result: "
                f"{result['result']}. "
                "Embedding not saved"
            )

        return duplicate_detection_success(
            result
        )

    except Exception as error:

        log_with_time(
            "❌ [check_duplicate_controller] "
            "Duplicate detection failed"
        )

        error_message(
            error
        )

        return throw_internal_server_error(
            error
        )