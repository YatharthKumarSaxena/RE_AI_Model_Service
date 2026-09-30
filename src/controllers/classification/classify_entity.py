from flask import request

from src.services.classification_service import (
    classify_entity
)

from src.responses.success.classification import (
    entity_type_classification_success
)

from src.responses.common.error_handler import (
    throw_internal_server_error
)

from src.utils.time_stamps import log_with_time
from src.utils.log_error import error_message


def classify_entity_controller():

    try:

        # ========================================================
        # GET REQUEST DATA
        # ========================================================

        request_data = request.get_json()

        # ========================================================
        # GET SELECTED MODEL
        # ========================================================

        entity_model = getattr(
            request,
            "entity_model",
            None
        )

        if not entity_model:
            raise ValueError(
                "Entity classification model not found."
            )

        # ========================================================
        # GET CONVERTED CONTENT
        # ========================================================

        converted_content = getattr(
            request,
            "converted_content",
            None
        )

        if not converted_content:
            raise ValueError(
                "Converted content not found."
            )

        # ========================================================
        # GET PROJECT CONTEXT
        # ========================================================

        project_title = request_data.get(
            "projectTitle"
        )

        project_description = request_data.get(
            "projectDescription"
        )

        problem_statement = request_data.get(
            "problemStatement"
        )

        project_goal = request_data.get(
            "projectGoal"
        )

        project_type = request_data.get(
            "projectType"
        )

        product_vision = request_data.get(
            "productVision"
        )

        # ========================================================
        # GET LLM-CONVERTED ENTITY CONTENT
        # ========================================================

        entity_title = converted_content.get(
            "title"
        )

        entity_description = converted_content.get(
            "description"
        )

        # ========================================================
        # CLASSIFICATION
        # ========================================================

        classification_result = classify_entity(
            project_title,
            project_description,
            problem_statement,
            project_goal,
            project_type,
            product_vision,
            entity_title,
            entity_description,
            entity_model
        )

        if not classification_result:
            raise ValueError(
                "Entity classification failed."
            )

        # ========================================================
        # SUCCESS
        # ========================================================

        log_with_time(
            "✅ [classify_entity_controller] "
            "Entity classified successfully"
        )

        return entity_type_classification_success(
            title=entity_title,
            description=entity_description,
            classification_result=classification_result
        )

    except Exception as error:

        log_with_time(
            "❌ [classify_entity_controller] "
            "Unexpected error while classifying entity."
        )

        error_message(error)

        return throw_internal_server_error(
            error
        )