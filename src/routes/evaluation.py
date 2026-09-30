from flask import Blueprint

from src.configs.uris import (
    EVALUATION_BASE,
    EVALUATION_ROUTES
)

from src.middlewares.common.verify_device_field import (
    verify_device_field
)

from src.controllers.evaluation.get_entity_classify_eval import (
    get_model_evaluation_controller
)


evaluation_bp = Blueprint(
    "evaluation",
    __name__,
    url_prefix=EVALUATION_BASE
)


# ============================================================
# MODEL EVALUATION
# ============================================================

@evaluation_bp.route(
    EVALUATION_ROUTES["MODEL_EVALUATION"],
    methods=["GET"]
)
def get_model_evaluation():

    result = verify_device_field()

    if result is not None:
        return result

    return get_model_evaluation_controller()